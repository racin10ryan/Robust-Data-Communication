import numpy as np
import os
import filesplit as splt
import pandas as pd

splitter = splt()

def packetize(path, filename, file_ext, chunksize, outputlocation):
    
    print("Opening file at {path}{filename}{file_ext} and splitting into parts...".format(filename = filename, path = path, file_ext = file_ext))
    
    splitter.split("{path}{filename}{file_ext}".format(filename = filename, path = path, file_ext = file_ext), chunksize, outputlocation)
    
    # Create Preamble to protect packet during sychronization process.

    preamble_arr = np.random.randint(2, 10000)
    preamble = bytes(preamble_arr)

    packet_arr = bytearray()
    packet_arr.extend(preamble)

    mgkstr = 'Packet Start'
    mgkstrbytes = bytes(mgkstr.encode())
    packet_arr.extend(mgkstrbytes)

    # Create cleanup list for convenient garbage collection.

    cleanup_list = []

    print("Writing manifest to packet...")

    # Write manifest to packet for file chunk length and number information.

    with open("{path}fs_manifest.csv".format(path = outputlocation), mode = 'rb') as file_to_read:
        file_bytes = bytes(file_to_read.read())
        packet_arr.extend(file_bytes)
        cleanup_list.append("{path}fs_manifest.csv".format(path = outputlocation))
    
    print("Writing file chunks to packet...")

    # Write file chunks with leading string identifying the start, end, and chunk number.

    i = 1
    while True:
        if os.path.isfile("{path}{filename}_{chunk_num}{file_ext}".format(chunk_num = i, path = outputlocation, filename = filename, file_ext = file_ext)):
            with open("{path}{filename}_{chunk_num}{file_ext}".format(chunk_num = i, path = outputlocation, filename = filename, file_ext = file_ext), mode = 'rb') as file_to_read:
                
                filestr = "File {num} Start".format(num = i)
                filestrbytes = bytes(filestr.encode())
                packet_arr.extend(filestrbytes)
                
                file_bytes = bytes(file_to_read.read())
                packet_arr.extend(file_bytes)

                filend = "File {num} End".format(num = i)
                filendbytes = bytes(filend.encode())
                packet_arr.extend(filendbytes)

                cleanup_list.append("{path}{filename}_{chunk_num}{file_ext}".format(chunk_num = i, path = outputlocation, filename = filename, file_ext = file_ext))
            i += 1
        else:
            break
    
    # Identify end of packet with string.

    mgkstrtoo = 'Packet End'
    mgkstrbytes = bytes(mgkstrtoo.encode())
    packet_arr.extend(mgkstrbytes)

    # Protect final useful bytes of packet with postamble because GNUradio is hungry.

    postamble_arr = np.random.randint(2, 100)
    postamble = bytes(postamble_arr)
    packet_arr.extend(postamble)

    packed_bytes = bytes(packet_arr)

    print("Saving packet.ddi...")

    with open("{outputlocation}\\packet.ddi".format(outputlocation = outputlocation), mode = 'wb') as file_to_write:
        file_to_write.write(packed_bytes)
    
    return cleanup_list # Return type is a list of file location strings to assist cleanup function.

def retransmit(request_list, filename, file_ext, outputlocation):

    if request_list[0] == 'all':
        packetize(request_list[1],request_list[2],request_list[3],request_list[4],request_list[5])

    else:
        # Create Preamble to protect packet during sychronization process.

        preamble_arr = np.random.randint(2, 10000)
        preamble = bytes(preamble_arr)

        packet_arr = bytearray()
        packet_arr.extend(preamble)

        mgkstr = 'Packet Start'
        mgkstrbytes = bytes(mgkstr.encode())
        packet_arr.extend(mgkstrbytes)

        # Write the requested files to packet

        for request in request_list:

            with open("{path}{filename}_{chunk_num}{file_ext}".format(chunk_num = request, path = outputlocation, filename = filename, file_ext = file_ext), mode = 'rb') as file_to_read:
                    
                filestr = "File {num} Start".format(num = request)
                filestrbytes = bytes(filestr.encode())
                packet_arr.extend(filestrbytes)
                
                file_bytes = bytes(file_to_read.read())
                packet_arr.extend(file_bytes)

                filend = "File {num} End".format(num = request)
                filendbytes = bytes(filend.encode())
                packet_arr.extend(filendbytes)
        # Identify end of packet with string.

        mgkstrtoo = 'Packet End'
        mgkstrbytes = bytes(mgkstrtoo.encode())
        packet_arr.extend(mgkstrbytes)

        # Protect final useful bytes of packet with postamble because GNUradio is hungry.

        postamble_arr = np.random.randint(2, 100)
        postamble = bytes(postamble_arr)
        packet_arr.extend(postamble)

        packed_bytes = bytes(packet_arr)

        print("Saving packet.ddi...")

        with open("{outputlocation}\\packet.ddi".format(outputlocation = outputlocation), mode = 'wb') as file_to_write:
            file_to_write.write(packed_bytes)

    return

def cleanup(cleanuplist): # This is run to clean up the folder when the whole packet has been received
    print("Cleaning up folder...")
    
    for garbage in cleanuplist:
        os.remove(garbage)
    return

def depacketize(filelocation):
    
    # initialize request list for damaged packets
    
    requestlist = []

    # Open File at filelocation

    with open(filelocation, mode = 'rb') as packet:
        packetarray = bytearray(packet.read())

    if packetarray.find('Packet Start'.encode()) != -1:

        # Read file until you find the packet start string
        startbytes = packetarray.find('Packet Start'.encode())
        endbytes = packetarray.find('File 1 Start'.encode())
        manifestbytes = packetarray[startbytes + len('Packet Start'.encode()):endbytes]

    else:
        requestlist = ['manifest']
        return requestlist

    with open('D:\\fs_manifest.csv', mode = 'wb') as manifest_to_write:
        manifest_to_write.write(manifestbytes)

    # Read data from manifest for number of chunks and length of chunks

    manifest_frame = pd.read_csv('D:\\fs_manifest.csv', index_col = 0)

    shape_of_manifest = manifest_frame.shape

    file_chunk_num = shape_of_manifest[0]

    # Search for file chunks by file strings
    for i in range(file_chunk_num):
        if packetarray.find('File {num} Start'.format(num = i).encode()) != -1:    

            startbytes = packetarray.find('File {num} Start'.format(num = i).encode())
            startbytesLen = len('File {num} Start'.format(num = i).encode())
            endbytes = packetarray.find('File {num} End'.format(num = i).encode())
            chunk_bytes = packetarray[startbytes + startbytesLen:endbytes]

            if len(chunk_bytes) != manifest_frame.iloc[i,1]:
                requestlist.append(i)
                continue
            elif len(chunk_bytes) == manifest_frame.iloc[i,1]:         
                with open('D:\\Figure_1_{num}.png'.format(num = i), mode = 'wb') as chunk_to_write:
                    chunk_to_write.write(chunk_bytes)

        else:
            requestlist.append(i)
            continue

    # requestlist.append for each file number missing and each file of wrong length

    return requestlist




    



