"""
File Name: modulation.py
Author: Joe Peterson
Date: 5 Apr 2008

Purpose:  Convert binary strings into sample arrays of carrier modulations.

Usage:

from modulation import *
dummyclass = mskMod(samples, symperiod, frequency)
dummyclass.run(binaryString)

samples:  The number of samples of the waveform in one symbol period
symperiod:  The duration of one symbol period
frequency:  The modulation carrier frequency
"""

import numpy as N
import pylab as PL
import scipy as S

class mskMod:
    def __init__(self, samples = 10000, symperiod = .001, frequency = 1000):
        self.samples = samples  #Set samples, period & frequency as attributes
        self.period = symperiod
        self.frequency = frequency
        self.freqs = {}  #Define a dictionary with the two modulation frequencies
        self.freqs['0'] = self.frequency + .25/self.period
        self.freqs['1'] = self.frequency - .25/self.period
        self.phase = N.pi/2  #Start a phase memory element
        self.lastbit = '0'  #Remember the last bit, to adjust phase
    def mskMod(self, binary = '0'):
        symbol = {'0':-1, '1':1}  #These are used in the msk symbol equation
        changelookup = {'00':0, '01':1, '10':1, '11':0}  #Used to determine bit differential
        self.change = changelookup[self.lastbit + binary]  #Bit differential
        t = N.arange(0, self.period, self.period/self.samples)  #Initialize a time array
        self.phase += .5 * N.pi * symbol[binary]  #Adjust the phase based on bit
        waveform = N.cos(2*N.pi*self.freqs[binary]*t - self.phase - N.pi * self.change)  #msk equation
        return(t, .5*waveform)
    def run(self, binaryString, plot = False):
	arraylist = []
	phasearray = N.zeros(len(binaryString))
	for i in range(len(binaryString)):
	    arraylist.append(self.mskMod(binary = binaryString[i])[1])
	    phasearray[i] = self.phase
	waveform = N.hstack(tuple(arraylist))
        if plot:  #Create a plot to inspect the generated waveform
            PL.subplot(2,1,1)
	    PL.plot(waveform)
	    PL.subplot(2,1,2)
	    PL.plot(phasearray)
	    PL.show()
	return(waveform[0:self.samples*len(binaryString)])

class bpskMod:
    def __init__(self, samples = 10000, symperiod = .001, frequency = 1000):
        self.samples = samples  #Set samples, period & frequency as attributes
        self.period = symperiod
        self.frequency = frequency
    def bpskMod(self, binary = '0'):
	lookupdict = {'0':1, '1':0}
	symbol = lookupdict[binary]
	t = N.arange(self.samples) * self.period/self.samples  #Generate time array
	waveform = N.cos(2 * S.pi * self.frequency * t + symbol * S.pi) #Calculates dependent variable 
	return(t, .5* waveform)
    def run(self, binaryString, plot = False):
	arraylist = []
        for i in range(len(binaryString)):
            arraylist.append(self.bpskMod(binary = binaryString[i])[1])
	    waveform = N.hstack(tuple(arraylist))
        if plot:  #Create a plot to inspect the generated waveform
	    PL.plot(waveform)
	    PL.show()
	return(waveform)
	     
class qpskMod:
    def __init__(self, samples = 10000, symperiod = .001, frequency = 1000):
        self.samples = samples  #Set samples, period & frequency as attributes
        self.period = symperiod
        self.frequency = frequency
    def qpskMod(self, binary = '00'):
	lookupdict = {'00':0, '01':1, '10':2, '11':3}
	symbol = lookupdict[binary]
	t = N.arange(self.samples * 2) * self.period/self.samples #Generate the time array
	waveform = N.cos(2 * S.pi * self.frequency * t + symbol * S.pi/2)  #This line calculates the dependent variable 
	return(t, .5*waveform)
    def run(self, binaryString, plot = False):
	arraylist = []
	for i in range(len(binaryString)/2):
	    arraylist.append(self.qpskMod(binary = binaryString[2*i:2*i+2])[1])
	waveform = N.hstack(tuple(arraylist))
        if plot:  #Create a plot to inspect the generated waveform
            PL.plot(waveform)
	    PL.show()
	return(waveform)
