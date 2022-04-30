#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
import os
import signal
import time
import subprocess
from gnuradio import digital
import tkinter as tk
from tkinter import filedialog
# import packtizeme as packet


#create server objects
print("STARTING XMLR SERVER - RADIO 1 TX")
rd1TxServer=subprocess.Popen('python txr1.py', shell=True)
print(rd1TxServer.pid)
time.sleep(2)
print("CONNECTING...")
rd1Tx = ServerProxy('http://'+'localhost'+':8000')
rd1Tx.stop()
print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED")

#print("STARTING XMLR SERVER - RADIO 1 RX")
#rd1RxServer=subprocess.Popen('python rxr1.py', shell=True)
#time.sleep(2)
#print("CONNECTING...")
#rd1Rx = ServerProxy('http://'+'localhost'+':8001')
#rd1Rx.stop()
#print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED")

#print("STARTING XMLR SERVER - RADIO 2 TX")
#rd2TxServer=subprocess.Popen('python txr2.py', shell=True)
#time.sleep(2)
#print("CONNECTING...")
#rd2Tx = ServerProxy('http://'+'localhost'+':8002')
#rd2Tx.stop()
#print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED")

print("STARTING XMLR SERVER - RADIO 2 RX")
rd2RxServer=subprocess.Popen('python rxr2.py', shell=True)
time.sleep(2)
print("CONNECTING...")
rd2Rx = ServerProxy('http://'+'localhost'+':8003')
rd2Rx.stop()
print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED")

#variables
#CONSTANTS - DO NOT CHANGE
#constellations
bpsk = digital.constellation_bpsk().base()
qpsk = digital.constellation_qpsk().base()
sixteenQAM = digital.constellation_16qam().base()

#frequencies
lowband = 9.15e6
midband = 2.45e9
highband = 5.85e9
			
#amplification
#lowband
#BPSK
lbTXbpsk = 1/50
lbIFbpsk = 47
lbBBbpsk = 25
#QPSK
lbTXqpsk = 1/50
lbIFqpsk = 47
lbBBqpsk = 25
#16 QAM
lbTXstQAM = 1/50
lbIFstQAM = 47
lbBBstQAM = 25
#midband
#BPSK
mbTXbpsk = 1/50
mbIFbpsk = 30
mbBBbpsk = 0
#QPSK
mbTXqpsk = 1/50
mbIFqpsk = 47
mbBBqpsk = 25
#16 QAM
mbTXstQAM = 1/50
mbIFstQAM = 47
mbBBstQAM = 25
#highband
#BPSK
hbTXbpsk = 1/50
hbIFbpsk = 47
hbBBbpsk = 25
#QPSK
hbTXqpsk = 1/50
hbIFqpsk = 47
hbBBqpsk = 25
#16 QAM
hbTXstQAM = 1/50
hbIFstQAM = 47
hbBBstQAM = 25

# Decision Variables
constellationDecision = bpsk
frequencyDecision = midband
transmitDivider = 1/50
receiverIFgain = 30
receiverBBgain = 0
currentTx = rd1Tx
currentRx = rd2Rx
fileName = ""
fileLocation = ""

#function defintions 
def changeFreq():
	currentTx.set_freq(frequencyDecision)
	currentRx.set_freq(frequencyDecision)
		
def changeConstell():
	currentTx.set_payload_chosen_constellation(constellationDecision)
	currentRx.set_payload_chosen_constellation(constellationDecision)
	
def changeAmp():
	setAmp()
	currentTx.set_transmit_divider(transmitDivider)
	currentRx.set_rxIF(receiverIFgain)
	currentRx.set_rxBB(receiverBBgain)
			
def changeFile(fileData):
	currentTx.set_file(fileData)
		
def changeTx(radio):
	if radio == rd1Tx:
		currentTx = rd1Tx
		currentRx = rd2Rx
	else:
		currentTx = rd2Tx
		currentRx = rd1Rx
			
def selectFreq(selectedFreq):
	if selectedFreq == "LOW":
		frequencyDecision = lowband
	elif selectedFreq == "MID":
		frequencyDecision = midband
	elif selectedFreq == "HIGH":
		frequencyDecision = highband
			
def selectConstell(selectedConstell):
	if selectedConstell == "BPSK":
		constellationDecision = bpsk
	elif selectedConstell == "QPSK":
		constellationDecisionn = qpsk
	elif selectedConstell == "16QAM":
		constellationDecision = sixteenQAM
			
def setAmp():
	if frequencyDecision == lowband:
		if constellationDecision == bpsk:
			transmitDivider = lbTXbpsk
			receiverIFgain = lbIFbpsk
			receiverBBgain = lbBBbpsk 
		elif constellationDecision == qpsk:
			transmitDivider = lbTXqpsk
			receiverIFgain = lbIFqpsk
			receiverBBgain = lbBBqpsk 
		elif constellationDecision == sixteenQAM:
			transmitDivider = lbTXstQAM
			receiverIFgain = lbIFstQAM
			receiverBBgain = lbBBstQAM
				
	elif frequencyDecision == midband:
		if constellationDecision == bpsk:
			transmitDivider = mbTXbpsk
			receiverIFgain = mbIFbpsk
			receiverBBgain = mbBBbpsk 
		elif constellationDecision == qpsk:
			transmitDivider = mbTXqpsk
			receiverIFgain = mbIFqpsk
			receiverBBgain = mbBBqpsk 
		elif constellationDecision == sixteenQAM:
			transmitDivider = mbTXstQAM
			receiverIFgain = mbIFstQAM
			receiverBBgain = mbBBstQAM
				
	elif frequencyDecision == highband:
		if constellationDecision == bpsk:
			transmitDivider = hbTXbpsk
			receiverIFgain = hbIFbpsk
			receiverBBgain = hbBBbpsk 
		elif constellationDecision == qpsk:
			transmitDivider = hbTXqpsk
			receiverIFgain = hbIFqpsk
			receiverBBgain = hbBBqpsk 
		elif constellationDecision == sixteenQAM:
			transmitDivider = hbTXstQAM
			receiverIFgain = hbIFstQAM
			receiverBBgain = hbBBstQAM

def getSelectedFrequency():
	return frequencyDecision
	
def getSelectedConstellation():
	return constellationDecision
			
def getFileName():
	return fileName
	
def getFileLocation():
	return fileLocation

def browseFiles():
	fileName = filedialog.askopenfilename(initialdir="/",title="Select a File", filetypes=(("Text files", "*.txt*"),("all files", "*.*")))
	# Change label contents
	label_file_explorer.configure(text="File Opened: "+fileName)


def turnOn():
	currentRx.start()
	time.sleep(2)
	currentTx.start()

def rd1Tord2():
	if fileName != "":
		changeTx(rd1Tx)
		selectFreq("LOW")
		selectConstell("BPSK")
		changeFreq()
		changeConstell()
		changeAmp()
		changeFile(fileName)
	else:
		print("No File Selected")
	
def rd2Tord1():
	if fileName != "":
		changeTx(rd1Tx)
		selectFreq("MID")
		selectConstell("BPSK")
		changeFreq()
		changeConstell()
		changeAmp()
		changeFile(fileName)
	else:
		print("No File Selected")
		print(rd1Rx.get_freq())

def closeProgram():
	os.kill(rd1TxServer.pid+1, signal.SIGSTOP)
	print(rd1TxServer.poll())
	#os.kill(rd1RxServer.pid, signal.SIGSTOP)
	#os.kill(rd2TxServer.pid, signal.SIGSTOP)
	os.kill(rd2RxServer.pid+1, signal.SIGSTOP)
	print(rd2RxServer.poll())
	quit()
	
	
	
#run
#rd1Tx.stop()
#rd1Rx.stop()
#rd2Tx.stop()
#rd2Rx.stop()

window = tk.Tk()
window.title('SDR: Robust Communication')
window.resizable(0, 0)


label_file_explorer = tk.Label(window, text="Select File to Transmit", width=100, height=4, fg="blue")

button_explore = tk.Button(window, text="Browse Files", command=browseFiles)

btnTxROne = tk.Button(window, text="Transmit From Radio 1 To Radio 2", command=rd1Tord2)

btnTxRTwo = tk.Button(window, text="Transmit From Radio 2 To Radio 1" , command=rd2Tord1)

button_exit = tk.Button(window, text="Exit", command=closeProgram)



label_file_explorer.grid(column=0, row=1)
button_explore.grid(column=0, row=2, pady=10)
btnTxROne.grid(column=0, row=3, padx=5, sticky=tk.W)
btnTxRTwo.grid(column=0, row=3, padx=5, sticky=tk.E)
button_exit.grid(column=0, row=4, pady=10)


window.mainloop()
	
