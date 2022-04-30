#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
from gnuradio import gr
import os
import signal
import time
import subprocess
from gnuradio import digital
import tkinter as tk
from tkinter import filedialog

tempFreqVariable = "LOW"
tempConstellVariable = "BPSK"


class Control():
   ######################################## Create Server Objects ########################################
    rd1Tx = ServerProxy('http://'+'localhost'+':8000')
    rd1Rx = ServerProxy('http://'+'localhost'+':8001')
    rd2Tx = ServerProxy('http://'+'localhost'+':8002')
    rd2Rx = ServerProxy('http://'+'localhost'+':8003')

    #######################################################################################################
    ###################################### CONSTANTS - DO NOT CHANGE ######################################
    #######################################################################################################


    ##################################### frequencies #####################################
    lowband = 9.15e6
    midband = 2.45e9
    highband = 5.85e9

    #################################### amplification ####################################
    ############################## lowband ##############################
    ################## BPSK ##################
    lbTXbpsk = 1/50
    lbIFbpsk = 47
    lbBBbpsk = 25
    ################## QPSK ##################
    lbTXqpsk = 1/50
    lbIFqpsk = 47
    lbBBqpsk = 25
    ################# 16 QAM #################
    lbTXstQAM = 1/50
    lbIFstQAM = 47
    lbBBstQAM = 25

    ############################### midband  #############################
    ################## BPSK ##################
    mbTXbpsk = 1/50
    mbIFbpsk = 30
    mbBBbpsk = 0
    ###### QPSK ######
    mbTXqpsk = 1/50
    mbIFqpsk = 47
    mbBBqpsk = 25
    ##### 16 QAM #####
    mbTXstQAM = 1/50
    mbIFstQAM = 47
    mbBBstQAM = 25

    ############################## highband ##############################
    ################## BPSK ##################
    hbTXbpsk = 1/50
    hbIFbpsk = 47
    hbBBbpsk = 25
    ################## QPSK ##################
    hbTXqpsk = 1/50
    hbIFqpsk = 47
    hbBBqpsk = 25
    ################# 16 QAM #################
    hbTXstQAM = 1/50
    hbIFstQAM = 47
    hbBBstQAM = 25
    #######################################################################################################
    #######################################################################################################

    ######################################### Decision Variables ##########################################
    constellationDecision = None
    frequencyDecision = None
    transmitDivider = None
    receiverIFgain = None
    receiverBBgain = None
    serverRd1 = None
    serverRd2 = None
    currentRd1 = None
    currentRd2 = None
    currentTx = None
    currentRx = None
    fileName = ""
    fileLocation = ""

    ######################################### Function Defintions #########################################
    def __init__(self):
        self.constellationDecision = self.bpsk
        self.frequencyDecision = self.lowband
        self.transmitDivider = self.lbTXbpsk
        self.receiverIFgain = self.lbIFbpsk
        self.receiverBBgain = self.lbBBbpsk
        self.setRadio("RD1","RX")
        self.setRadio("RD2","RX")



    ################################### XMLR Functions ###################################
    def changeFreq(self):
        #Change Radio 1's Frequency
        print("Configuring R1's Frequency...")
        self.currentRd1.set_freq(self.frequencyDecision)
        #Change Radio 2's Frequency
        print("Configuring R2's Frequency...")
        self.currentRd2.set_freq(self.frequencyDecision)
		
    def changeConstell(self):
        #Change Radio 1's Constellation
        print("Configuring R1's Constellation...")
        self.currentRd1.changeConstellations(self.constellationDecision)
        #Change Radio w's  Constellation
        print("Configuring R12's Constellation...")
        self.currentRd2.changeConstellations(self.constellationDecision)
	
    def changeAmp(self):
        #set amplification variables based on current Frequency and Constellation
        self.setAmp(self)
        self.txORrx(self)
        if self.currentTx != None and self.currentRx !=None:
            print("Configuring Amplification...")
            self.currentTx.set_transmit_divider(self.transmitDivider)
            self.currentRx.set_rxIF(self.receiverIFgain)
            self.currentRx.set_rxBB(self.receiverBBgain)
        else:
            print("ERROR: Both Radios Functions are the Same")
			
    def changeFile(self):
        self.txORrx(self)
        print("Loading File...")
        self.currentTx.set_file(fileLocation)

    def startRadios(self):
        #start radios
        print("Staring Radios...")
        time.sleep(3)
        self.txORrx(self)
        if self.currentTx != None and self.currentRx !=None:
            self.currentRx.start()
            time.sleep(3)
            self.currentTx.restart()
        else:
            self.currentRd1.start()
            self.currentRd2.start()

    def stopRadios(self):
        #stop radios
        print("Stoping Radios...")
        self.currentRd1.stop()
        self.currentRd2.stop()

    ############################### Set Variable Functions ###############################
    def selectFreq(self,selectedFreq):
        #Take string input to set variable to corresponding Frequency
        print("Selecting Frequency...")
        print()
        if selectedFreq == "LOW":
            self.frequencyDecision = self.lowband
        elif selectedFreq == "MID":
            self.frequencyDecision = self.midband
        elif selectedFreq == "HIGH":
            self.frequencyDecision = self.highband
			
    def selectConstell(self, selectedConstell):
        #Take string input to set variable to corresponding Frequency
        ###########################probably take out ################
        print("Selecting Constellation...")
        self.constellationDecision = selectedConstell

			
    def setAmp(self):
        #set amplification variables based on current frequency and constellation
        print("Selecting Amplification...")
        # If LowBand
        if self.frequencyDecision == self.lowband:
            # If Lowband and BPSK
            if self.constellationDecision == "BPSK":
                self.transmitDivider = self.lbTXbpsk
                self.receiverIFgain = self.lbIFbpsk
                self.receiverBBgain = self.lbBBbpsk
            # If Lowband and QPSK 
            elif self.constellationDecision == "QPSK":
                self.transmitDivider = self.lbTXqpsk
                self.receiverIFgain = self.lbIFqpsk
                self.receiverBBgain = self.lbBBqpsk 
            # If Lowband and 16 QAM
            elif self.constellationDecision == "16QAM":
                self.transmitDivider = self.lbTXstQAM
                self.receiverIFgain = self.lbIFstQAM
                self.receiverBBgain = self.lbBBstQAM

	    # if Midband			
        elif self.frequencyDecision == self.midband:
            # If Midband and BPSK
            if self.constellationDecision == "BPSK":
                self.transmitDivider = self.mbTXbpsk
                self.receiverIFgain = self.mbIFbpsk
                self.receiverBBgain = self.mbBBbpsk
            # If Midband and QPSK 
            elif self.constellationDecision == "QPSK":
                self.transmitDivider = self.mbTXqpsk
                self.receiverIFgain = self.mbIFqpsk
                self.receiverBBgain = self.mbBBqpsk 
            # If Midband and 16 QAM
            elif self.constellationDecision == "16QAM":
                self.transmitDivider = self.mbTXstQAM
                self.receiverIFgain = self.mbIFstQAM
                self.receiverBBgain = self.mbBBstQAM

	    # If Highband	
        elif self.frequencyDecision == self.highband:
            # If Highband and BPSK
            if self.constellationDecision == "BPSK":
                self.transmitDivider = self.hbTXbpsk
                self.receiverIFgain = self.hbIFbpsk
                self.receiverBBgain = self.hbBBbpsk 
            # If Highband and QPSK
            elif self.constellationDecision == "QPSK":
                self.transmitDivider = self.hbTXqpsk
                self.receiverIFgain = self.hbIFqpsk
                self.receiverBBgain = self.hbBBqpsk 
            # If Highband and 16 QAM
            elif self.constellationDecision == "16QAM":
                self.transmitDivider = self.hbTXstQAM
                self.receiverIFgain = self.hbIFstQAM
                self.receiverBBgain = self.hbBBstQAM

    ############################### Radio Control Functions ##############################
    def setRadio(self, radioVariable, radioType):
        # create a temp variable to stop server
        xmlrControl=None
        # Depending on which radio and Tx or Rx
        # Set currentRd1 or currentRd2, xmlrControl
        # And start server
        print("STARTING XMLR SERVER")
        if radioVariable == "RD1":
            if self.serverRd1 != None:
                self.serverKill(self.serverRd1)
            if radioType == "TX":
                self.currentRd1 = self.rd1Tx
                xmlrControl = self.rd1Tx
                self.serverRd1=subprocess.Popen('python txr1.py', shell=True)
            elif radioType == "RX":
                self.currentRd1 = self.rd1Rx
                xmlrControl = self.rd1Rx
                self.serverRd1=subprocess.Popen('python rx1.py', shell=True)
        elif radioVariable == "RD2":
            if self.serverRd2 != None:
                self.serverKill(self.serverRd2)
            if radioType == "TX":
                self.currentRd2 = self.rd2Tx
                xmlrControl = self.rd2Tx
                self.serverRd2=subprocess.Popen('python txr2.py', shell=True)
            elif radioType == "RX":
                self.currentRd2 = self.rd2Rx
                xmlrControl = self.rd2Rx
                self.serverRd2=subprocess.Popen('python rxr2.py', shell=True)
        print("CONNECTING...")
        # Wait for server to start
        time.sleep(5)
        # Stop server
        xmlrControl.stop()
        print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED: "+radioVariable+" - "+radioType)

    def configureRadios(self):
        #configure the radio before transmission
        self.selectFreq(self, tempFreqVariable)
        self.selectConstell(self,tempConstellVariable)
        self.changeFreq(self)
        self.changeConstell(self)
        self.changeAmp(self)
        self.changeFile(self)


    def txORrx(self):
        # Determine if Radios are Tx or Rx
        self.currentTx = None
        self.currentRx = None
        print("Determining Tx and Rx")
        if self.currentRd1 == self.rd1Tx:
            self.currentTx = self.rd1Tx
        elif self.currentRd1 == self.rd1Rx:
            self.currentRx = self.rd1Rx
        if self.currentRd2 == self.rd2Tx:
            self.currentTx = self.rd2Rx
        elif self.currentRd2 == self.rd2Rx:
            self.currentRx = self.rd2Rx

    def serverKill(serverToKill):
        #kill Server
        if serverToKill != None:
            os.kill(serverToKill.pid, signal.SIGSTOP)
            os.kill(serverToKill.pid+1, signal.SIGSTOP)

################################################### Main ##################################################
def main(top_block_cls=Control):

    ct = top_block_cls

    ################################## GUI Functions ####################################
    def browseFiles():
        global fileLocation
        # Open File Explorer
        fileLocation = filedialog.askopenfilename(initialdir="/",title="Select a File", 
        filetypes=(("Text files", "*.txt*"),("all files", "*.*")))
	    # Change label contents
        label_file_explorer.configure(text="File Opened: "+fileLocation)

    def rd1Tord2():
        # If there is a selected file
        if fileLocation != "":
            ct.setRadio(ct,"RD1","TX")
            ct.setRadio(ct,"RD2","RX")
            ct.configureRadios(ct)
            ct.startRadios(ct)
        # If no file is selected
        else:
            print("No File Selected")
	
    def rd2Tord1():
        # If there is a selected file
        if fileLocation != "":
            ct.setRadio(ct,"RD1","TX")
            ct.setRadio(ct,"RD2","RX")
            ct.configureRadios(ct)
            ct.startRadios(ct)
        # If no file is selected
        else:
            print("No File Selected")

    def closeProgram():
        # Kill both radio's 
        ct.serverKill(ct.serverRd1)
        ct.serverKill(ct.serverRd2)
        # exit main
        quit()

    ######################################## GUI  #########################################
    window = tk.Tk()
    label_file_explorer = tk.Label(window, text="Select File to Transmit", width=100, height=4, fg="blue")
    button_explore = tk.Button(window, text="Browse Files", command=browseFiles)
    btnTxROne = tk.Button(window, text="Transmit From Radio 1 To Radio 2", command=rd1Tord2)
    btnTxRTwo = tk.Button(window, text="Transmit From Radio 2 To Radio 1" , command=rd2Tord1)
    button_exit = tk.Button(window, text="Exit", command=closeProgram)
    
    ################################## GUI Configuration ##################################
    label_file_explorer.grid(column=0, row=1)
    button_explore.grid(column=0, row=2, pady=10)
    btnTxROne.grid(column=0, row=3, padx=5, sticky=tk.W)
    btnTxRTwo.grid(column=0, row=3, padx=5, sticky=tk.E)
    button_exit.grid(column=0, row=4, pady=10)
    
    ######################################### Loop ########################################
    window.mainloop()

if __name__ == '__main__':
    main()