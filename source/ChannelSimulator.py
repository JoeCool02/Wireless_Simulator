#!/usr/bin/env python
"""
File Name: ChannelSimulator.py
Author: Joe Peterson
Date: 5 Apr 2008

Purpose:  This is the main executable file for the channel simulator for linux.  
It displays a GUI with the following categories for altering the channel:

Pulse Shaping
Modulation
Fading
Noise

Adjusting the values of the GUI first stops the current simulation session.  Next
the program repopulates the arrays defining the pulses, waveform, and channel.  Finally, 
it restarts the simulation.  

Usage:

Run this program from the linux command line or gnome 

"""

from rayleighfade import *
from awgn import *
from demodulator import *
from channelaudio import *
from time import *
from symboldict import *
import threading, Queue
import os
 
class channelsim:
    def __init__(self, **args): 
        for i in args:
            setattr(self, i, args[i])
        reqvals = ['carrierfreq', 'symperiod', 'pulsetype', 'alpha', 'modtype',
                   'fading', 'awgn', 'audsamprate']
        self.reqtext = {'carrierfreq': "carrierfreq is int",
                   'symperiod': "symperiod is float",
                   'pulsetype' : "pulsetype is str 'raisedCos' or 'rect'",
                   'alpha' : "alpha is float between 0 and 1",
                   'modtype' : "modtype is str 'bpsk', 'qpsk', or 'msk'",
                   'fading': "fading is boolean True or False",
                   'awgn' : "awgn is boolean True or False",
                   'audsamprate' : "audsamprate is int, 11025 for speech",
                   'maxdoppler' : "maxdoppler is int",
                   'seqlength' : "seqlength is int.  represents length of fading impulse response",
                   'samplerate' : "samplerate is int.  represents sample rate for fading impulse response",
                   'power' : "power is int.  represents power of the AWGN noise"}
        self.evalreq(reqvals)
        fadereqvals = ['maxdoppler', 'seqlength', 'samplerate']        
        if self.fading:
            self.evalreq(fadereqvals)
        awgnreqvals = ['power']
        if self.awgn:
            self.evalreq(awgnreqvals)
        self.setupConstants()
        self.setupObjects()
    def setupConstants(self):
        self.samplesperperiod = 10 * self.carrierfreq * self.symperiod           
    def setupObjects(self):
        self.symbolLookupTable = symbolLookupTable(self.pulsetype, self.modtype, self.samplesperperiod,
                                                   self.symperiod, self.alpha, self.carrierfreq)
        self.symbolFinder = self.symbolLookupTable.symbolDict                                           
        self.audio = AudioInterface(self.audsamprate)
        if self.fading:        
            self.fadingobject = rayleighFade(self.symperiod, self.samplesperperiod, self.samplerate,
                                         self.maxdoppler, self.seqlength)
        if self.awgn:
            self.noiseobject = awgnGen(self.symperiod, self.samplesperperiod, self.power)
        self.demodulator = demodulator(self.symbolFinder)      
    def evalreq(self, reqvals):
        for i in reqvals:
            try:
                getattr(self, i)
            except:
                print '%s must have a value.  %s' % (i, self.reqtext[i])
    def passAudioThruChannel(self):
        print "Recording..."
        thissample = []
        thatsample = []
        for i in range(11025):
             thissample.append(self.audio.sampleGrab())
        print "Processing..."  
        print time()
        print len(thissample)      
        for i in thissample:
            thisarray = self.symbolFinder[i]
            if self.fading:            
                thisarray = self.fadingobject.run(thisarray)
            if self.awgn:            
                thisarray = self.noiseobject.run(thisarray)
            thatsample.append(self.demodulator.run(thisarray))
        print time()
        for i in thatsample:        
            self.audio.samplePut(i)
    def run(self):
       
        print "Working..."
        self.passAudioThruChannel()
                                    
def main():
    cs = channelsim(carrierfreq = 10000, symperiod = .001, pulsetype = 'raisedCos', alpha = .75,
                    modtype = 'qpsk', fading = True, awgn = True, audsamprate = 11025, 
                    maxdoppler = 200, seqlength = 200, samplerate = 100000, power = 1000)
    cs.run()
    exit()    
    
if __name__ == "__main__":
    main()
    exit()