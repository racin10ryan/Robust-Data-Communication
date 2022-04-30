# Robust-Data-Communication
This project checks for interference on three channels. After ranking the power levels, the channel with the lowest power level is chosen to transmit on.

Used two HackRF One Radios for testing

Dependencies:
  -Radioconda: https://github.com/ryanvolz/radioconda
      (Be sure to udpate HackRF Library to latest version)
  - Latest version of HackRF firmware and library: https://github.com/greatscottgadgets/hackrf
  - Other dependencies may be needed. Just check the imports in new_main.py


PC1 folder and PC2 folder are the same files. Just put 1 copy on each PC. Within new_main.py, you will have to change the the IP in line 28:
self.server = SimpleXMLRPCServer(("other_pc_ip_address", 8006), allow_none=True)

Both PC's have to be running before you are allowed to transmit.

Note: HackRF one does not have automatic gain control and because OFDM is used, you will have to manually test different amplifications for different channels and
constellations (aim for a receive signal strength of -35 dB). As it stands right now, the only constellation used is BPSK and does 3 channels in the 915MHz ISM band. 
You will have to uncomment self.changeConstell() in configureRadios function definition and manually set the constellation by the tempConstell Variable
("BPSK", "QPSK","16QAM"). Choose different channels by changinglowband, midband, and highband variables. Osmocom likes a signal within the range of -1 and 1 so 
you will have to divide the signal depending on constellation chosen on transmit flowgraph. Threshhold of schmidl & cox sync is very sensitive as well (receive side,
deconstruct_packet_new hierarchy block to be more specific). If the threshold is too low, you will drop packets even if you aren't transmitting. If threshold is
set too high, you will never receive anything. Will have to adjust manually depending on frequency, constellation and amplifications. Because Forward Error Correction 
(LDPC) is used, 2MHz is the max sample rate that can be used without errors. This results in a 2 MHz bandwidth in the analog domain.  
