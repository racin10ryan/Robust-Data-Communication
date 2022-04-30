#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
from gnuradio import gr
import os
import signal
import time
import subprocess
import packetizeme as pk
import tkinter as tk
from tkinter import filedialog
import zmq
import numpy as np

tempFreqVariable = "HIGH"
tempConstellVariable = "BPSK"
_debug=1


class Control():
   ######################################## Create Server Objects ########################################
    rd1Tx = ServerProxy('http://'+'localhost'+':8000')
    rd1Rx = ServerProxy('http://'+'localhost'+':8001')
    rd2Tx = ServerProxy('http://'+'localhost'+':8002')
    rd2Rx = ServerProxy('http://'+'localhost'+':8003')
    rd1ZMQ = ServerProxy('http://'+'localhost'+':8004')
    rd2ZMQ = ServerProxy('http://'+'localhost'+':8005')

    ############################################# ZMQ Objects ############################################
    port_rd1 = '1234'
    port_rd2 = '1235'
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    #######################################################################################################
    ###################################### CONSTANTS - DO NOT CHANGE ######################################
    #######################################################################################################


    ##################################### frequencies #####################################
    lowband = 915e6
    midband = 2.45e9
    highband = 5.8e9

    #################################### amplification ####################################
    ############################## lowband ##############################
    ################## BPSK ##################
    lbTXbpsk = 1/10
    lbIFbpsk = 40
    lbBBbpsk = 0
    ################## QPSK ##################
    lbTXqpsk = 1/38
    lbIFqpsk = 40
    lbBBqpsk = 15
    ################# 16 QAM #################
    lbTXstQAM = 1/50
    lbIFstQAM = 40
    lbBBstQAM = 15

    ############################### midband  #############################
    ################## BPSK ##################
    mbTXbpsk = 1/50
    mbIFbpsk = 40
    mbBBbpsk =15
    ###### QPSK ######
    mbTXqpsk = 1/50
    mbIFqpsk = 40
    mbBBqpsk = 15
    ##### 16 QAM #####
    mbTXstQAM = 1/50
    mbIFstQAM = 40
    mbBBstQAM = 15

    ############################## highband ##############################
    ################## BPSK ##################
    hbTXbpsk = 1/10
    hbIFbpsk = 40
    hbBBbpsk = 0
    ################## QPSK ##################
    hbTXqpsk = 1/10
    hbIFqpsk = 40
    hbBBqpsk = 0
    ################# 16 QAM #################
    hbTXstQAM = 1/20
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

    zmqOn=None

    ######################################## Dictionary Variables #########################################
    dict_rd1 =	{
        "LOW": 0+0j,
        "MID": 0+0j,
        "HIGH": 0+0j
    } 
    dict_rd2 =	{
        "LOW": 0+0j,
        "MID": 0+0j,
        "HIGH": 0+0j
    }

    ######################################### Function Defintions #########################################
    def __init__(self):
        self.constellationDecision = "BPSK"
        self.frequencyDecision = self.lowband
        self.transmitDivider = self.lbTXbpsk
        self.receiverIFgain = self.lbIFbpsk
        self.receiverBBgain = self.lbBBbpsk
        self.setRadio("RD1","RX")
        self.setRadio("RD2","RX")
        self.startRadios("RD1","RX")


    ################################### XMLR Functions ###################################
    def changeFreq(self):
        #Change Radio 1's Frequency
        if _debug:
            print("Configuring R1's Frequency...")
        self.currentRd1.set_freq(self.frequencyDecision)
        #Change Radio 2's Frequency
        if _debug:
            print("Configuring R2's Frequency...")
        self.currentRd2.set_freq(self.frequencyDecision)
		
    def changeConstell(self):
        #Change Radio 1's Constellation
        if _debug:
            print("Configuring R1's Constellation...")
        self.currentRd1.changeConstellations(self.constellationDecision)
        #Change Radio w's  Constellation
        if _debug:
            print("Configuring R2's Constellation...")
        self.currentRd2.changeConstellations(self.constellationDecision)
	
    def changeAmp(self):
        #set amplification variables based on current Frequency and Constellation
        if _debug:
            print("In Change Amp")
        self.setAmp(self)
        self.txORrx(self)
        if _debug:
            print("If we are transmitting")
        if self.currentTx != None and self.currentRx !=None:
            if _debug:
                print("Configuring Tx/Rx Amplification...")
            self.currentTx.set_transmit_divider(self.transmitDivider)
            self.currentRx.set_rxIF(self.receiverIFgain)
            self.currentRx.set_rxBB(self.receiverBBgain)
        else:
            if _debug:
                print("Configuring Both Radio's Amplification...")
            self.currentRd1.set_rxIF(self.receiverIFgain)
            self.currentRd1.set_rxBB(self.receiverBBgain)
            self.currentRd2.set_rxIF(self.receiverIFgain)
            self.currentRd2.set_rxBB(self.receiverBBgain)

    def changeFile(self):
        self.txORrx(self)
        if _debug:
            print("Updating Tx File")
        self.currentTx.configureFile()

    def startRadios(self):
        #start radios
        if _debug:
            print("Staring Radios...")
        time.sleep(3)
        self.txORrx(self)
        if _debug:
            print(self.currentTx)
            print(self.currentRx)
        if self.currentTx != None and self.currentRx !=None:
            if _debug:
                print("If Transmit Mode")            
            if _debug:
                print("Enable Flow")
            self.currentRd1.enableFlow(True)
            self.currentRd2.enableFlow(True)
            if _debug:
                print("Staring Rx for Transmission...")
            self.currentRx.start()
            time.sleep(3)
            if _debug:
                print("Staring Tx for Transmission...")
            self.currentTx.start()
        elif self.currentRd1 != self.rd1ZMQ and self.currentRd2 !=self.rd2ZMQ:
            if _debug:
                print("Starting Both Radios")
            self.currentRd1.start()
            self.currentRd2.start()

    def stopRadios(self):
        #stop radios
        if _debug:
            print("Staring Radios...")
        self.txORrx(self)
        if _debug:
            print("If Transmit Mode")
        if self.currentTx != None and self.currentRx !=None:
            if _debug:
                 print("Disable Flow")
            self.currentRd1.enableFlow(False)
            self.currentRd2.enableFlow(False)
            if _debug:
                print("Stoping Transmission...")
            self.currentTx.stop()
            time.sleep(3)
            if _debug:
                print("Stopping Reception...")
            self.currentRx.stop()

        

    ############################### Set Variable Functions ###############################
    def selectFreq(self,selectedFreq="LOW",dictionary=None):
        #Take string input to set variable to corresponding Frequency
        if _debug:
            print("Selecting Frequency...")
            print("If there is a dictionary....")
        if dictionary != None:
            if _debug:
                print("Selecting Channel...")
            selectedFreq=min(dictionary, key=dictionary.get)
            if _debug:
                print("Dictionary selects: "+selectedFreq)
        if _debug:
                print("Selected Frequency is:")
        if selectedFreq == "LOW":
            if _debug:
                print("Low")
            self.frequencyDecision = self.lowband
        elif selectedFreq == "MID":
            if _debug:
                print("Mid")
            self.frequencyDecision = self.midband
        elif selectedFreq == "HIGH":
            if _debug:
                print("High")
            self.frequencyDecision = self.highband
			
    def selectConstell(self, selectedConstell):
        #Take string input to set variable to corresponding Frequency
        ###########################probably take out ################
        if _debug:
            print("Selecting Constellation...")
        self.constellationDecision = selectedConstell

			
    def setAmp(self):
        #set amplification variables based on current frequency and constellation
        if _debug:
            print("Selecting Amplification...")
        # If LowBand
        if self.frequencyDecision == self.lowband:
            if _debug:
                print("If Lowband Selected...")
            # If Lowband and BPSK
            if self.constellationDecision == "BPSK":
                if _debug:
                    print("Setting Lowband BPSK Amps...")
                self.transmitDivider = self.lbTXbpsk
                self.receiverIFgain = self.lbIFbpsk
                self.receiverBBgain = self.lbBBbpsk
            # If Lowband and QPSK 
            elif self.constellationDecision == "QPSK":
                if _debug:
                    print("Setting Lowband QPSK Amps...")
                self.transmitDivider = self.lbTXqpsk
                self.receiverIFgain = self.lbIFqpsk
                self.receiverBBgain = self.lbBBqpsk 
            # If Lowband and 16 QAM
            elif self.constellationDecision == "16QAM":
                if _debug:
                    print("Setting Lowband 16QAM Amps...")
                self.transmitDivider = self.lbTXstQAM
                self.receiverIFgain = self.lbIFstQAM
                self.receiverBBgain = self.lbBBstQAM

	    # if Midband			
        elif self.frequencyDecision == self.midband:
            if _debug:
                print("If Midband Selected...")
            # If Midband and BPSK
            if self.constellationDecision == "BPSK":
                if _debug:
                    print("Setting Midband BPSK Amps...")
                self.transmitDivider = self.mbTXbpsk
                self.receiverIFgain = self.mbIFbpsk
                self.receiverBBgain = self.mbBBbpsk
            # If Midband and QPSK 
            elif self.constellationDecision == "QPSK":
                if _debug:
                    print("Setting Midband QPSK Amps...")
                self.transmitDivider = self.mbTXqpsk
                self.receiverIFgain = self.mbIFqpsk
                self.receiverBBgain = self.mbBBqpsk 
            # If Midband and 16 QAM
            elif self.constellationDecision == "16QAM":
                if _debug:
                    print("Setting Midband 16QAM Amps...")
                self.transmitDivider = self.mbTXstQAM
                self.receiverIFgain = self.mbIFstQAM
                self.receiverBBgain = self.mbBBstQAM

	    # If Highband	
        elif self.frequencyDecision == self.highband:
            if _debug:
                print("If Highband Selected...")
            # If Highband and BPSK
            if self.constellationDecision == "BPSK":
                if _debug:
                    print("Setting Highband BPSK Amps...")
                self.transmitDivider = self.hbTXbpsk
                self.receiverIFgain = self.hbIFbpsk
                self.receiverBBgain = self.hbBBbpsk 
            # If Highband and QPSK
            elif self.constellationDecision == "QPSK":
                if _debug:
                    print("Setting Highband QPSK Amps...")
                self.transmitDivider = self.hbTXqpsk
                self.receiverIFgain = self.hbIFqpsk
                self.receiverBBgain = self.hbBBqpsk 
            # If Highband and 16 QAM
            elif self.constellationDecision == "16QAM":
                if _debug:
                    print("Setting Highband 16QAM Amps...")
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
        if _debug:
            print("STARTING XMLR SERVER")
        if radioVariable == "RD1":
            if _debug:
                print("If Radio 1....")
            if self.serverRd1 != None:
                if _debug:
                    print("Killing Radio's Previous Process...")
                self.serverKill(self.serverRd1)
            if radioType == "TX":
                if _debug:
                    print("Starting Tx Process for Rd1")
                self.currentRd1 = self.rd1Tx
                xmlrControl = self.rd1Tx
                self.serverRd1=subprocess.Popen('python txr1.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            elif radioType == "RX":
                if _debug:
                    print("Starting Rx Process for Rd1")
                self.currentRd1 = self.rd1Rx
                xmlrControl = self.rd1Rx
                self.serverRd1=subprocess.Popen('python rxr1.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            elif radioType == "ZMQ":
                if _debug:
                    print("Starting ZMQ Process for Rd1")
                self.currentRd1 = self.rd1ZMQ
                xmlrControl=self.rd1ZMQ
                self.serverRd1=subprocess.Popen('python rd1zmq.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
        elif radioVariable == "RD2":
            if _debug:
                print("If Radio 2")
            if self.serverRd2 != None:
                if _debug:
                    print("Killing Radio's Previous Process...")
                self.serverKill(self.serverRd2)
            if radioType == "TX":
                if _debug:
                    print("Starting Tx Process for Rd2")
                self.currentRd2 = self.rd2Tx
                xmlrControl = self.rd2Tx
                self.serverRd2=subprocess.Popen('python txr2.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            elif radioType == "RX":
                if _debug:
                    print("Starting Rx Process for Rd2")
                self.currentRd2 = self.rd2Rx
                xmlrControl = self.rd2Rx
                self.serverRd2=subprocess.Popen('python rxr2.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            elif radioType == "ZMQ":
                if _debug:
                    print("Starting ZMQ Process for Rd2")
                self.currentRd2 = self.rd2ZMQ
                xmlrControl=self.rd2ZMQ
                self.serverRd2=subprocess.Popen('python rd2zmq.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
        if _debug:
            print("CONNECTING...")
        # Wait for server to start
        time.sleep(5)
        # Stop server
        if radioType == "TX" or radioType == "RX":
            if _debug:
                print("If Radio is not in ZMQ Mode...")
                print("Stopping "+radioVariable+" - "+radioType)
            xmlrControl.stop()
        if _debug:
                print("CONNECTION SUCCESSFUL! FLOWGRAPGH STOPPED: "+radioVariable+" - "+radioType)

    def scan(self, freq):
        port=None
        dictionary=None
        if _debug:
            print("Scan with Both...")
        for num in range(2):
            if _debug:
                print("Loop for Radio "+str(num+1))
            if num==0:
                if _debug:
                    print("Selecting Correct Port and Dictionary for Radio 1...")
                port=self.port_rd1
                dictionary=self.dict_rd1
            elif num==1:
                if _debug:
                    print("Selecting Correct Port and Dictionary for Radio 2...")
                port=self.port_rd2
                dictionary=self.dict_rd2
            if _debug:
                print("Port Selected")
            temp_array= np.array([])
            self.socket.connect ("tcp://localhost:" + port)
            if _debug:
                print("Port Connected")
            self.socket.setsockopt_string(zmq.SUBSCRIBE,"")
            time.sleep(2)
            if _debug:
                print("Scanning....")
            t_end=time.time()+0.5
            while time.time()<t_end:
                #  Get the reply.
                self.s = self.socket.recv()
                message = np.frombuffer(self.s, dtype=np.complex64, count=-1)
                temp_array = np.append(temp_array,message)
            if _debug:
                print("Done Scanning")
            self.socket.disconnect("tcp://localhost:" + str(port))
            if _debug:
                print("Disconnected from ZMQ port "+port)
            power = 10*np.log((np.dot(np.conj(temp_array), temp_array))/temp_array.size)
            if _debug:
                print("Power Calculated")
            dictionary.update({freq: power})
            if _debug:
                print("Wrote to Dictionary")

    def packetizeFile(self):
        if _debug:
            print("Packetizing Selected File...")
        pk.packetize(self.fileLocation,"/media/ryan/New Volume/Senior Design/Working On/")

    def configureRadios(self,dict):
        #configure the radio before transmission
        if _debug:
            print("Configuring Radios")
        self.selectFreq(self, dictionary=dict )
        self.selectConstell(self,tempConstellVariable)
        self.changeFreq(self)
        self.changeConstell(self)
        self.changeAmp(self)
        self.changeFile(self)


    def txORrx(self):
        # Determine if Radios are Tx or Rx
        self.currentTx = None
        self.currentRx = None
        if _debug:
            print("Determining Tx and Rx")
        if self.currentRd1 == self.rd1Tx:
            self.currentTx = self.rd1Tx
        elif self.currentRd1 == self.rd1Rx:
            self.currentRx = self.rd1Rx
        if self.currentRd2 == self.rd2Tx:
            self.currentTx = self.rd2Tx
        elif self.currentRd2 == self.rd2Rx:
            self.currentRx = self.rd2Rx

    def serverKill(serverToKill):
        #kill Server
        if serverToKill != None:
            os.killpg(os.getpgid(serverToKill.pid), signal.SIGTERM)

################################################### Main ##################################################
def main(top_block_cls=Control):

    ct = top_block_cls

    ################################## GUI Functions ####################################
    def browseFiles():
        # Open File Explorer
        ct.fileLocation = filedialog.askopenfilename(initialdir="/",title="Select a File", 
        filetypes=(("Text files", "*.txt*"),("all files", "*.*")))
	    # Change label contents
        label_file_explorer.configure(text="File Opened: "+ct.fileLocation)

    def rd1Tord2():
        # If there is a selected file
        if ct.fileLocation != "":
            pk.packetize(ct.fileLocation,"/media/ryan/New Volume/Senior Design/Working On/")
            ct.setRadio(ct,"RD1","TX")
            ct.setRadio(ct,"RD2","RX")
            ct.configureRadios(ct, ct.dict_rd2)
            ct.startRadios(ct)
        # If no file is selected
        else:
            print("No File Selected")
	
    def rd2Tord1():
        # If there is a selected file
        if ct.fileLocation != "":
            pk.packetize(ct.fileLocation,"/media/ryan/New Volume/Senior Design/Working On/")
            ct.setRadio(ct,"RD1","RX")
            ct.setRadio(ct,"RD2","TX")
            ct.configureRadios(ct, ct.dict_rd1)
            ct.startRadios(ct)
        # If no file is selected
        else:
            print("No File Selected")

    def scanRadios(freq):
        ct.selectFreq(ct,selectedFreq=freq)
        ct.selectConstell(ct,"BPSK")
        ct.currentRd1.lock()
        ct.currentRd2.lock()
        ct.changeFreq(ct)
        ct.changeAmp(ct)
        ct.currentRd1.unlock()
        ct.currentRd2.unlock()
        ct.scan(ct, freq)


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
    ct.setRadio(ct,"RD1","ZMQ")
    ct.setRadio(ct,"RD2","ZMQ")
    scanRadios("LOW")
    scanRadios("MID")
    scanRadios("HIGH")
    print(ct.dict_rd1)
    print(ct.dict_rd2)
    window.mainloop()

if __name__ == '__main__':
    main()