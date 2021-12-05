#!/usr/bin/env python
"""
File Name: awgn.py
Author: Joe Peterson
Date: 13 Apr 2008

Purpose:  Takes waveform arrays as input and returns them with additive
white gaussian noise effects.  

Usage:

from awgn import *
awgninstance = awgn(period, samplesperperiod, power) 
outputarray = awgninstance.run(inputarray, plot = False)

period:  The symbol period of the expected signal inputs
power:  The average power of the awgn.
samplesperperiod:  The number of samples in each symbol period
"""

import numpy as N
import scipy as S
import pylab as PL
import numpy.random as R
from modulation import *

class awgnGen:
    def __init__(self, period = .001, samplesperperiod = 10000, power = 1):
        self.power = power
        self.period = period
        self.samples = samplesperperiod
    def run(self, signal, plot = False):
        self.length = len(signal)
        noise = R.randn(self.length)
        self.noisepower = N.sum(pow(noise, 2))*(self.samples/float(self.length))*(1/self.period)
        self.sigpower = N.sum(pow(signal, 2))*(self.samples/float(self.length))*(1/self.period)
        noise = noise * N.sqrt(self.power/self.noisepower)
        self.noisepower = N.sum(pow(noise, 2))*(self.samples/float(self.length))*(1/self.period)
        self.snrdb = 10*N.log10(self.sigpower/float(self.noisepower))
        waveform = signal + noise        
        if plot:
           PL.plot(noise)
           PL.plot(signal + 4)
           PL.show()
        return waveform
        
if __name__=='__main__':
    samples = 200   
    qm = qpskMod(samples = samples)
    signal = qm.run('00011011')
    for i in range(5):
        PL.subplot(5,1,i)
        awgn = awgnGen(power = pow(10,2*i), samplesperperiod = samples)
        PL.plot(awgn.run(signal))
        PL.title('SNR = %s dB' % int(awgn.snrdb))
    PL.show()
        
    