#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
rd1Rx = ServerProxy('http://'+'localhost'+':8000') 

rd1Rx.stop()

def startRadios():
    serverR1.start()
    serverR2.start()

def stopRadios():
    serverR1.stop()
    serverR2.stop()

def radioStatus():
    currentTx = None
    currentRx = None
    if serverRd1 == rd1Tx:
        currentTx = serverRd1
    else:
        currentRx = serverRd1
    if serverRd2 == rd2Tx:
        currentTx = serverRd2
    else:
        currentRx = serverRd2

def check():
    if currentTx == None or currentRx == None:
        return False
    else: 
        return True

def changeRadios(newRd1, newRd2):
    stopRadios()
    if serverR1 != newRd1:
        os.kill(serverR1.pid+1, signal.SIGSTOP)
        os.kill(serverR1.pid, signal.SIGSTOP)
        serverR1=newRd1
        
        time.sleep(2)
        serverR1.stop()
    if serverR2 != newRd2:
        os.kill(serverR2.pid+1, signal.SIGSTOP)
        os.kill(serverR2.pid, signal.SIGSTOP)
        serverR2=newRd2
        time.sleep(2)
        serverR2.stop()
    radioStatus()

    



