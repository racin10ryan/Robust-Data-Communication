#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
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
import threading
import pathlib
from filesplit.merge import Merge


tempFreqVariable = "HIGH"
tempConstellVariable = "BPSK"
_debug=1

class Control():
    def __init__(self, constell="BPSK", freq=915.e6 ):
        ######################################### Create XMLRPC Server ########################################
        #Computer 1
        self.server = SimpleXMLRPCServer(("192.168.254.37", 8006), allow_none=True)
        #self.server = SimpleXMLRPCServer(("localhost", 8006), allow_none=True)
        #Computer 2
        #self.server = SimpleXMLRPCServer(("localhost", 8007)), allow_none=True)
        ################################## Register Functions #################################
        self.server.register_instance(self)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        ######################################## Create Server Objects ########################################
        self.Tx = ServerProxy('http://'+'localhost'+':8002')
        self.Rx = ServerProxy('http://'+'localhost'+':8001')
        #Computer 1
        self.rdZMQ = ServerProxy('http://'+'localhost'+':8004')
        self.other = ServerProxy('http://'+'192.168.254.133'+':8007')
        #self.other = ServerProxy('http://'+'localhost'+':8007')
        #Computer 2
        #self.ZMQ = ServerProxy('http://'+'localhost'+':8005')
        #self.other = ServerProxy('http://'+'localhost'+':8006')

        ############################################# ZMQ Objects ############################################
        #Computer 1
        self.port = '1234'
        #Computer 2
        #self.port = '1235'

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)

        #######################################################################################################
        ###################################### CONSTANTS - DO NOT CHANGE ######################################
        #######################################################################################################


        ##################################### frequencies #####################################
        self.lowband = 908e6
        self.midband = 915e6
        self.highband = 922e6

        #################################### amplification ####################################
        ############################## lowband ##############################
        ################## BPSK ##################
        self.lbTXbpsk = 1/50
        self.lbRxThresh=925e-3
        self.lbIFbpsk = 0
        self.lbBBbpsk = 0
        ################## QPSK ##################
        self.lbTXqpsk = 1/75
        self.lbIFqpsk = 0
        self.lbBBqpsk = 0
        ################# 16 QAM #################
        self.lbTXstQAM = 1/25
        self.lbIFstQAM = 0
        self.lbBBstQAM = 0

        ############################### midband  #############################
        ################## BPSK ##################
        self.mbTXbpsk = 1/50
        self.mbRxThresh=925e-3
        self.mbIFbpsk = 0
        self.mbBBbpsk =0
        ###### QPSK ######
        self.mbTXqpsk = 1/75
        self.mbIFqpsk = 0
        self.mbBBqpsk = 0
        ##### 16 QAM #####
        self.mbTXstQAM = 1/25
        self.mbIFstQAM = 0
        self.mbBBstQAM = 0

        ############################## highband ##############################
        ################## BPSK ##################
        self.hbTXbpsk = 1/47
        self.hbRxThresh=.94
        self.hbIFbpsk = 0
        self.hbBBbpsk = 0
        ################## QPSK ##################
        self.hbTXqpsk = 1/75
        self.hbIFqpsk = 0
        self.hbBBqpsk = 0
        ################# 16 QAM #################
        self.hbTXstQAM = 1/25
        self.hbIFstQAM = 0
        self.hbBBstQAM = 0
        #######################################################################################################
        #######################################################################################################

        ######################################### Decision Variables ##########################################
        self.constellationDecision = constell
        self.frequencyDecision = freq
        self.transmitDivider = self.lbTXbpsk
        self.receiverThresh=0
        self.receiverIFgain = 0
        self.receiverBBgain = 0
        self.currentServer=None
        self.currentControl=None
        self.fileLocation = ""

        ######################################## Dictionary Variables #########################################
        self.dictTable =	{
            "LOW": 0+0j,
            "MID": 0+0j,
            "HIGH": 0+0j
        } 
    
    ################################### XMLR Functions ###################################
    def changeFreq(self):
        #Change Radio 1's Frequency
        if self.currentControl == self.Tx or self.currentControl ==  self.Rx:
            if _debug:
                print("Configuring This Radio's Frequency...")
            self.currentControl.set_freq(self.frequencyDecision)
        else:
            self.rdZMQ.set_freq(self.frequencyDecision)

    def changeConstell(self):
        #Change Radio 1's Constellation
        if self.currentControl == self.Tx or self.currentControl ==  self.Rx:
            if _debug:
                print("Configuring This Radio's Constellation...")
            self.currentControl.changeConstellations(self.constellationDecision)

	
    def changeAmp(self):
        #set amplification variables based on current Frequency and Constellation
        if self.currentControl == self.Tx or self.currentControl ==  self.Rx:
            if _debug:
                print("In Change Amp")
            self.setAmp()
            if _debug:
                print("Configuring Tx/Rx Amplification...")
            if self.currentControl == self.Tx:
                self.currentControl.set_transmit_divider(self.transmitDivider)
                self.other.setAmp()
        else:
            self.currentControl.set_rxIF(0)
            self.currentControl.set_rxBB(0)


    def startRadios(self):
        #start radios
        if _debug:
            print("Starting Radios...")        
        if _debug:
            print("Enable Flow")
        self.currentControl.enableFlow(True)
        if _debug and self.currentControl == self.Tx:
                print("Staring Tx for Transmission...")
        self.currentControl.start()
        if _debug:
            print("STARTED")   
        
        

    def stopRadios(self):
        #stop radios
        if _debug:
            print("Stoping Radios...")
        if _debug:
            print("Disable Flow")
        self.currentControl.enableFlow(False)
        if _debug and self.currentControl == self.Tx:
            print("Stoping Transmission...")
        self.currentControl.stop()



    ############################### Set Variable Functions ###############################
    def selectFreq(self,fromDictionary,selectedFreq,):
        #Take string input to set variable to corresponding Frequency
        if _debug:
            print("Selecting Frequency...")
            print("If there is a dictionary....")
        if fromDictionary:
            if _debug:
                print("Selecting Channel...")
            selectedFreq=min(self.dictTable, key=self.dictTable.get)
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
        if fromDictionary:
            return(selectedFreq)
			
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
                self.receiverThresh=self.lbRxThresh
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
                self.receiverThresh=self.mbRxThresh
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
                self.receiverThresh=self.hbRxThresh
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
    def setRadio(self, radioType):
        # create a temp variable to stop server
        # Depending on which radio and Tx or Rx
        # Set currentRd1 or currentRd2, xmlrControl
        # And start server
        if _debug:
            print("STARTING XMLR SERVER")                    
            print("If there is another server open...")
        if self.currentControl != None:
            if _debug:
                print("Killing Radio's Previous Process...")
            self.serverKill()
            time.sleep(2)
            os.system('hackrf_spiflash -R')
        if radioType == "TX":
            if _debug:
                print("Starting Tx Process")
            self.currentControl = self.Tx
            self.currentServer=subprocess.Popen(
                ('python tx.py --freq '+str(self.frequencyDecision)), 
                stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            #self.currentServer=subprocess.Popen('python tx.py', stdout=subprocess.PIPE, 
                #shell=True, preexec_fn=os.setsid)
        elif radioType == "ZMQ":
            if _debug:
                print("Starting ZMQ Process")
            self.currentControl=self.rdZMQ
            self.currentServer=subprocess.Popen('python rd1zmq.py', stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
        if _debug:
            print("CONNECTING...")
        # Wait for server to start
        # Stop server
        #if radioType == "TX":
            #if _debug:
                #print("If Radio is not in ZMQ Mode...")
                #print("Stopping Transmitter...")
            #self.currentControl.stop()

    def setReceiver(self):
        if _debug:
            print("STARTING XMLR RECEIVE SERVER")                    
            print("If there is another server open...")
        if self.currentControl != None:
            if _debug:
                print("Killing Radio's Previous Process...")
            self.serverKill()
            time.sleep(2)
            os.system('hackrf_spiflash -R')
        if _debug:
            print("Starting Rx Process")
        self.currentControl = self.Rx
        if _debug:
            print("Current Control Set")
        self.currentServer=subprocess.Popen(
            ('python rx.py --freq '+str(self.frequencyDecision)+' --rxThresh '+str(self.receiverThresh)), 
            stdout=subprocess.PIPE, 
            shell=True, preexec_fn=os.setsid)
        if _debug:
            print("Receiver Opened")

    def zmqCheck(self):
        time.sleep(5)
        self.scanRadio("LOW")
        self.scanRadio("MID")
        self.scanRadio("HIGH")
        if _debug:
            freqList=self.dictTable.keys()
            for freq in freqList:
                print('{key} : {power:.3}dB'.format(key = freq, power = self.dictTable.get(freq)))

    def scanRadio(self,freq):
        self.selectFreq(False,freq)
        if _debug:
            print("Locking")
        self.currentControl.lock()
        if _debug:
            print("Changing frequency")
        self.changeFreq()
        self.changeAmp()
        self.currentControl.unlock()
        self.scan(freq)

    def scan(self, freq):
        if _debug:
            print("Scan "+str(freq)+"...")
        temp_array= np.array([])
        self.socket.connect ("tcp://localhost:" + self.port)
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
        self.socket.disconnect("tcp://localhost:" + str(self.port))
        if _debug:
            print("Disconnected from ZMQ port "+self.port)
        power = 10*np.log((np.dot(np.conj(temp_array), temp_array))/temp_array.size)
        if _debug:
            print("Power Calculated")
        self.dictTable.update({freq: np.real(power)})
        if _debug:
            print("Wrote to Dictionary")

    def packetizeFile(self):
        if _debug:
            print("Packetizing Selected File...")
        pk.packetize(self.fileLocation,os.getcwd)

    def configureRadios(self):
        #configure the radio before transmission
        if _debug:
            print("Configuring Radios")
        temp=self.other.selectFreq(True,"LOW")
        print(temp)
        self.selectFreq(False,temp)
        self.selectConstell(tempConstellVariable)
        self.setAmp()
        self.other.selectConstell(tempConstellVariable)
        self.other.setAmp()
        #self.changeFreq()
        #self.changeConstell()
        #self.changeAmp()
        #self.currentControl.configureFile()
        
    def cleanUpReceiver(self,location):
        mergercv = Merge(str(os.getcwd())+'\Receive', str(os.getcwd())+'\Receive', 'output'+location.suffix)
        mergercv(cleanup=True)

    def getMissing(self,name):
        myarray = (pk.depacketize((str(os.getcwd())+'/Received/received.ddi'),(str(os.getcwd())+'/Received/{filename}'.format(filename=name))))
        if _debug:
            print(myarray)
        return myarray

    def serverKill(self):
        #kill Server
        if self.currentServer != None:
            try:
                os.killpg(os.getpgid(self.currentServer.pid), signal.SIGTERM)
            except:
                if _debug:
                    print("No Process Open")
            self.currentServer = None




################################################### Main ##################################################
def main(top_block_cls=Control(freq=915.e6)):

    ct = top_block_cls

    ################################## GUI Functions ####################################
    def browseFiles():
        # Open File Explorer
        ct.fileLocation = filedialog.askopenfilename(initialdir="/",title="Select a File", 
        filetypes=(("Text files", "*.txt*"),("all files", "*.*")))
	    # Change label contents
        label_file_explorer.configure(text="File Opened: "+ct.fileLocation)

    def transmit():
        # If there is a selected file
        label_update.configure(text="Transmitting...")
        if ct.fileLocation != "":
            filepath = pathlib.PurePath(ct.fileLocation)
            pk.packetize(ct.fileLocation,str(os.getcwd()))
            if _debug:
                print("Receiver Started")
            ct.setRadio("TX")
            while True:
                ct.configureRadios()
                #ct.startRadios()
                ct.setRadio("TX")
                time.sleep(1)
                if _debug:
                    print("Starting Receiver")
                ct.other.setReceiver()
                print(ct.currentServer)
                poll=ct.currentServer.poll()
                print(poll)
                while poll is None:
                    time.sleep(1)
                    poll=ct.currentServer.poll()
                ct.serverKill()
                time.sleep(5)
                ct.other.setRadio("ZMQ")
                received= (ct.other.getMissing(filepath.name))
                if not received:
                    label_update.configure(text="Done!")
                    break
                else:
                    pk.retransmit(received,ct.fileLocation,str(os.getcwd()))
                    ct.other.zmqCheck()
                    label_update.configure(text="Retransmitting...")
            ct.other.cleanUpReceiver(ct.fileLocation)
            mergexmt = Merge(filepath.parent, filepath.parent, filepath.name)
            mergexmt.merge(cleanup=True)
            #pk.cleanup(cleanup)

        # If no file is selected
        else:
            print("No File Selected")
                

    def closeProgram():
        # Kill both radio's 
        ct.serverKill()
        # exit main
        quit()

    ######################################## GUI  #########################################
    window = tk.Tk()
    label_file_explorer = tk.Label(window, text="Select File to Transmit", width=100, height=4, fg="blue")
    button_explore = tk.Button(window, text="Browse Files", command=browseFiles)
    btnTxROne = tk.Button(window, text="Transmit", command=transmit)
    label_update = tk.Label(window, text="", width=100, height=4, fg="black")
    button_exit = tk.Button(window, text="Exit", command=closeProgram)
    
    ################################## GUI Configuration ##################################
    label_file_explorer.grid(column=0, row=1)
    label_update.grid(column=0, row=2, pady=10)
    button_explore.grid(column=0, row=3, pady=10)
    btnTxROne.grid(column=0, row=4, pady=10)
    button_exit.grid(column=0, row=5, pady=10)
    
    ######################################### Loop ########################################
    ct.setRadio("ZMQ")
    #ct.setRadio(ct,"RD2","ZMQ")
    ct.zmqCheck()
    window.mainloop()

if __name__ == '__main__':
    main()