#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy

Rx = ServerProxy('http://'+'localhost'+':8001')

Rx.lock()
#Rx.set_freq(922e6)
Rx.enableFlow(True)
Rx.unlock()