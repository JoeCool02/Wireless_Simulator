#!/usr/bin/env python
"""
File Name: rayleighfade.py
Author: Joe Peterson
Date: 5 Apr 2008

Purpose:  Take waveform arrays as input and returns them with fading
effects.  Stores information beyond Ts and adds it to subsequent waveforms.

Usage:

from rayleighfade import *
rfinstance = rayleighfade(period, samplesperperiod, samplerate, maxdoppler, seqlength) 
outputarray = rfinstance.run(inputarray)

period:  The period of the incoming symbols
samplesperperiod:  The number of samples in each of those periods
samplerate: The sampling rate of the generated rayleigh fading.
maxdoppler:  The maximum frequency shift due to doppler effects.
seqlength:  The length of the PDP decayed to 1%. 
"""

import numpy as N
import scipy as S
import pylab as PL
import numpy.random as R
import numpy.fft as F
from modulation import *

class rayleighFade:
    def __init__(self, period = .001, samplesperperiod = 2000, samplerate = 100000, 
                 maxdoppler = 20000, seqlength = 2000):
        self.period = period  #Copy some of the input args to attributes
        self.maxdoppler = maxdoppler
        self.samplerate = samplerate
        self.seqlength = pow(2, int(N.log2(seqlength))+3)  #IFFT is fastest working with power of 2
        self.seqlength2 = seqlength  #Still need the desired sequence length -- this is decay to 1%
        self.spectrumlow = -self.maxdoppler * self.seqlength/self.samplerate+.5  #Upper & lower spreading bounds
        self.spectrumhigh = -self.spectrumlow
        self.length = int(N.ceil(seqlength/samplesperperiod+1))  #The number of multipath echoes in fading sequence
        self.tau = (seqlength/float(samplesperperiod))*period/4.6  #Exponential PDP delay constant
        self.alpha = 1/N.sqrt(N.sum(N.exp(-N.arange(self.length)*self.period/self.tau))) #Exponential PDP amplitude constant
        self.tauarray = N.ceil(N.arange(self.length)*self.tau*samplesperperiod/period) #PDP amplitude for each multipath
        self.alphaarray = self.alpha * N.exp(-N.arange(self.length)*self.period*2/self.tau) #Convert tau to samples
        self.ISI = N.array([])  #Set up array to store ISI/multipath from past signals
        self.samples = samplesperperiod
        '''print self.tau
        print self.alpha        
        print self.tauarray
        print self.alphaarray'''
    def dopplerSpectrum(self):
        '''Generates Doppler Spectrum'''
        f = N.arange(self.spectrumlow + 1,self.spectrumhigh, 1)  
        self.randvarlength = len(f)
        term1 = f/(self.maxdoppler*self.seqlength/self.samplerate)
        term1 = 1-pow(term1,2)
        term1 = pow(term1, .25)
        psdarray = 1/term1
        return psdarray
    def genRandomVar(self):
        '''Generates a sequence of complex random variables'''
        randreal = R.randn(self.randvarlength)*1+0j
        randimag = R.randn(self.randvarlength)*0+1j
        randseq = randreal + randimag
        return randseq
    def runFourier(self, psdarray, randseq, plot = False):
        '''Multiplies PSD by complex random values, then executes an inverse fourier transform.
        The waveform returned is an array of length seqlength.'''
        waveformlen = 2*self.seqlength        
        tempwaveform = psdarray * randseq  
        waveform = F.ifft(tempwaveform, waveformlen)
        waveformpower = N.sum(pow(N.hypot(waveform.real, waveform.imag),2))*N.sqrt(self.seqlength2)        
        waveform = waveform/waveformpower
        waveform = N.hypot(waveform.real, waveform.imag)
        waveform = waveform[self.seqlength-.5*self.seqlength2:self.seqlength+.5*self.seqlength2]
        if plot:   
            PL.subplot(3,1,2)
            PL.title('h(t,tau) samples')        
            PL.plot(waveform)
        return waveform
    def run(self, signal = [0], plot = False):        
        psd = self.dopplerSpectrum()
        self.tempoutput = []
        for i in range(self.length):
            randvar = self.genRandomVar() 
            fading = self.runFourier(psd, randvar, plot)
            delayedsignal = N.hstack((N.zeros(int(self.tauarray[i])),signal))            
            self.tempoutput.append(self.alphaarray[i]*N.convolve(delayedsignal,fading))
            PL.subplot(3,1,3)
            PL.title('Multi-Path Components')        
            PL.plot(N.convolve(delayedsignal,fading))
        waveform = N.zeros((self.length+1, len(self.tempoutput[-1])))
        for i in range(self.length):
            waveform[i, 0:len(self.tempoutput[i])] = self.tempoutput[i]
        waveform[self.length,0:len(self.ISI)] = self.ISI
        waveform = N.sum(waveform, 0)
        sigpower = N.sum(pow(signal,2))
        waveformpower = N.sum(pow(waveform,2))
        print sigpower, waveformpower
        if plot:
            PL.subplot(3,1,1)
            PL.plot(signal+2, label = 'QPSK (Amplitude Offset)')
            PL.plot(waveform, label = 'Channel Output')
            PL.legend(('QPSK (Amplitude Offset)', 'Channel Output'), loc = 'upper right')
            PL.xlabel('Samples')
            PL.title('''Effect of MultiPath Rayleigh Fading, period = %s, tau = %s, 
                      fd = %sHz''' % (self.period, self.tau, self.maxdoppler))           
            PL.show()
        self.ISI = waveform[len(signal):]    
        return waveform[0:len(signal)]
        
if __name__=='__main__':
    samples = 2000  
    qm = qpskMod(samples = samples)
    signal = qm.run('00011011')
    for i in range(5):
        PL.subplot(5,1,i+1)
        rf = rayleighFade(seqlength = 200, samplesperperiod = samples, maxdoppler = 100*(i+1))
        PL.plot(rf.run(signal))
    PL.show()
        