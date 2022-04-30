import packetizeme 
import os

requestlist=packetizeme.depacketize('/media/ryan/New Volume/Senior Design/Working On/PC2/Received/received.ddi','/media/ryan/New Volume/Senior Design/Working On/PC2/Received/input.wav')
print(requestlist)
#print((str(os.getcwd())))
#packetizeme.retransmit(requestlist,'/home/ryan/Documents/Tests/input.txt',(str(os.getcwd()+'/Received')))
#requestlist=requestlist=packetizeme.depacketize('/media/ryan/New Volume/Senior Design/Working On/PC2/Received/packet.ddi','/media/ryan/New Volume/Senior Design/Working On/PC2/Received/input.txt')
#print(requestlist)

#os.system('hackrf_spiflash -R')