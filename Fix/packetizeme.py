import numpy as np
import os
import filesplit.split as splitit
import pandas as pd
import pathlib
import numpy as np
from collections import Counter

# TODO: Cleanup is a mess, needs to be reworked to make sense. Hack works for now.

def packetize(inputlocation,outputlocation):
    
    # use pathlib to split the file paths into convenient parts

    inputpath = pathlib.PurePath(inputlocation)
    filename = inputpath.stem
    file_ext = inputpath.suffix
    inputfolder = inputpath.parent

    outputpath = pathlib.PurePath(outputlocation)

    cleanup_list = [inputpath, outputpath]

    print("Opening file at {filepath} and splitting into parts...".format(filepath = inputpath))

    # TODO: calculate chunk size by filesize, determine maximum file size to be sent.
    
    splitter = splitit.Split(inputpath, inputpath.parent)
    splitter.bysize(1024)
    
    # Create Preamble to protect packet during sychronization process.

    preamble_arr = np.random.randint(2, 1000000)
    preamble = bytes(preamble_arr)

    packet_arr = bytearray()
    packet_arr.extend(preamble)

    print("Writing manifest to packet...")
    for _ in range(11):
        mgkstr = 'Packet Start'
        mgkstrbytes = bytes(mgkstr.encode())
        packet_arr.extend(mgkstrbytes)

        # Write manifest to packet for file chunk length and number information.

        with open(pathlib.PurePath(inputfolder, 'manifest'), mode = 'rb') as file_to_read:
            file_bytes = bytes(file_to_read.read())
            packet_arr.extend(file_bytes)
            cleanup_list.append(pathlib.PurePath(outputpath, 'manifest'))
        
        mgkstr = 'Manifest End'
        mgkstrbytes = bytes(mgkstr.encode())
        packet_arr.extend(mgkstrbytes)
        
    print("Writing file chunks to packet...")

    # Write file chunks with leading string identifying the start, end, and chunk number.

    i = 1

    
    while True:
        if os.path.isfile(pathlib.PurePath(inputfolder, '{filename}_{chunk_num}{file_ext}'.format(filename = filename, chunk_num = i, file_ext = file_ext))):
            with open(pathlib.PurePath(inputfolder, '{filename}_{chunk_num}{file_ext}'.format(filename = filename, chunk_num = i, file_ext = file_ext)), mode = 'rb') as file_to_read:
                
                filestr = "File {num} Start".format(num = i)
                filestrbytes = bytes(filestr.encode())
                packet_arr.extend(filestrbytes)
                
                file_bytes = bytes(file_to_read.read())
                packet_arr.extend(file_bytes)

                filend = "File {num} End".format(num = i)
                filendbytes = bytes(filend.encode())
                packet_arr.extend(filendbytes)

                cleanup_list.append(pathlib.PurePath(outputpath,'{name}_{num}{ext}'.format(name = filename, num = i, ext = file_ext)))
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

    with open(pathlib.PurePath(outputpath, 'packet.ddi'), mode = 'wb') as file_to_write:
        file_to_write.write(packed_bytes)
    
    return cleanup_list # Return type is a list of file location strings to assist cleanup function.

def retransmit(request_list, inputlocation, outputlocation):

    inputpath = pathlib.PurePath(inputlocation)
    path = inputpath.parent
    filename = inputpath.stem
    file_ext = inputpath.anchor

    if request_list[0] == 'manifest':
        # Create Preamble to protect packet during sychronization process.

        preamble_arr = np.random.randint(2, 10000)
        preamble = bytes(preamble_arr)

        packet_arr = bytearray()
        packet_arr.extend(preamble)

        mgkstr = 'Packet Start'
        mgkstrbytes = bytes(mgkstr.encode())
        packet_arr.extend(mgkstrbytes)


        print("Writing manifest to packet...")

        # Write manifest to packet for file chunk length and number information.print(pathlib.PurePath(inputfolder, '{filename}_{chunk_num}{file_ext}'.format(filename = filename, chunk_num = i, file_ext = file_ext)))
        packet_arr.extend(mgkstrbytes)

        # Write the requested files to packet

        for request in request_list:

            with open("{folder}{filename}_{chunk_num}{file_ext}".format(chunk_num = request, folder = path, filename = filename, file_ext = file_ext), mode = 'rb') as file_to_read:
                    
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

def depacketize(filelocation, outputlocation):
    
    # initialize request list for damaged packets
    
    requestlist = []

    
    filepath = pathlib.PurePath(filelocation)
    outputpath = pathlib.PurePath(outputlocation)
    filefolder = outputpath.parent
    filename = outputpath.stem
    file_ext = outputpath.suffix

    # Open File at filelocation
    with open(filepath, mode = 'rb') as packet:
        packetarray = bytearray(packet.read())

    man_list = []
    man_len_list = []

    if packetarray.find('Packet Start'.encode()) != -1:
        while packetarray.find('Packet Start'.encode()) != -1:

            # Read file until you find the packet start string
            startbytes = packetarray.find('Packet Start'.encode())
            endbytes = packetarray.find('Manifest End'.encode())
            manifestbytes = packetarray[startbytes + len('Packet Start'.encode()):endbytes]
            man_list.append(manifestbytes)
            man_len_list.append(len(manifestbytes))
            startbytes = packetarray.find('Packet Start'.encode())
            startbytesLen = len('Packet Start'.encode())
            endbytes = packetarray.find('Manifest End'.encode())
            packetarray = packetarray[startbytes + startbytesLen:endbytes]
        counts = Counter(man_len_list)
        manifestbytes = man_list.index(counts.most_common())

    else:
        requestlist = ['manifest']
        return requestlist

    with open(pathlib.PurePath(filefolder,'manifest'), mode = 'wb') as manifest_to_write:
        manifest_to_write.write(manifestbytes)

    # Read data from manifest for number of chunks and length of chunks

    manifest_frame = pd.read_csv(pathlib.PurePath(filefolder, 'manifest'), index_col = 0)

    shape_of_manifest = manifest_frame.shape

    file_chunk_num = shape_of_manifest[0]

    print(shape_of_manifest)

    # Search for file chunks by file strings
    for i in range(1,file_chunk_num + 1):

        strloc = packetarray.find('File {num} Start'.format(num = i).encode())
        if strloc != -1:    

            startbytes = packetarray.find('File {num} Start'.format(num = i).encode())
            startbytesLen = len('File {num} Start'.format(num = i).encode())
            endbytes = packetarray.find('File {num} End'.format(num = i).encode())
            chunk_bytes = packetarray[startbytes + startbytesLen:endbytes]

            chunklen = len(chunk_bytes)

            if chunklen != manifest_frame.iloc[i-1,0]:
                requestlist.append(i)
                continue
            elif chunklen == manifest_frame.iloc[i-1,0]:         
                with open(pathlib.PurePath(filefolder,'{name}_{num}{ext}'.format(name = filename, num = i, ext = file_ext)), mode = 'wb') as chunk_to_write:
                    chunk_to_write.write(chunk_bytes)

        else:
            requestlist.append(i)

    # requestlist.append for each file number missing and each file of wrong length

    return requestlist

    # TODO: Request list should become a dictionary that can be used for both retransmit requests and cleanup.
    # TODO: Need merge function in this library that simplifies the function call to func(location of packet)