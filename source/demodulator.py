#!/usr/bin/env python
"""
File Name: demodulator.py
Author: Joe Peterson
Date: 13 Apr 2008

Purpose:  Takes waveform arrays as input and returns their
estimated binary string.  

Usage:

from demodulator import *
demodinstance = demodulator() 
outputstring = demodinstance.run(inputarray)

period:  The symbol period of the expected signal inputs
power:  The average power of the awgn.
samplesperperiod:  The number of samples in each symbol period
"""

import numpy as N
import scipy as S
import pylab as PL
#from modulation import *
#from symboldict import *
#from awgn import *
import time

class demodulator:
    def __init__(self, symboldict):
        self.symboldict = symboldict
    def run(self, signal):
        decisiondict = {}
        decisionstatmatrix = N.zeros(len(self.symboldict))
        counter = 0
        for i in self.symboldict:
            newdecisionstat = N.sum(self.symboldict[i]*signal)
            decisiondict[newdecisionstat] = i
            decisionstatmatrix[counter] = newdecisionstat
            counter += 1 
        symbol = decisiondict[N.amax(decisionstatmatrix)]
        return symbol
        
if __name__=='__main__':
    samples = 2000    
    slt = symbolLookupTable(samples = samples)
    signal = slt.symbolDict['10011010']
    dm = demodulator(slt.symbolDict)
    for i in range(100):    
        awgn = awgnGen(power = 10, samplesperperiod = samples)
        signal = awgn.run(signal)
        print dm.run(signal)           
    