"""
File Name: pulses.py
Author: Joe Peterson
Date: 5 Apr 2008

Purpose:  Create arrays representing various pulse shapes.  Pulse 
shapes currently available:

Raised Cosine
Rectangular

Usage:

from pulses import *
rcinstance = raisedCosine(alpha, period, samples, numperiods)
rcinstance.run()

or

from pulses import *
rectinstance = rect(alpha, period, samples, numperiods)
rectinstance.run()

alpha:  A factor in the raised cosine class that determines rolloff.  Unused in rect.
symperiod:  The duration of one symbol period
samples: The number of samples per period in the array returned
numperiods:  The number of symbol periods in the array returned 
"""

import numpy as N
import scipy as S
import pylab as PL

class raisedCosine:
    def __init__(self, alpha = .99, period = .001, samples = 2000, numperiods = 8):
        self.alpha = alpha
        self.period = period
        self.numperiods = numperiods * 2
        self.samples = samples * numperiods
    def raisedCos(self):        
        t = N.arange(self.samples) * self.period/self.samples * self.numperiods#Generate the time array
        t = t - self.period * self.numperiods / 2 #Shift the array to the left to center the pulse on time = 0
        term1 = N.sinc(t/self.period)/self.period  #The next four lines calculate the dependent variable
        term2 = N.cos((t * self.alpha * S.pi)/self.period)
        term3 = 1 - pow((4 * self.alpha * t) / (2 * self.period),2)
        tempformula = term1 * term2 / term3
        t = t + self.period * self.numperiods / 2  #Shift the pulse back over so it's causal
        formula = N.zeros(len(t)) #Create a new array to hold a series of pulses
        shiftvar = 2*self.samples/self.numperiods #Define shift variable to move pulses in time
        a = len(t) #Variable for the upper index limit of the pulse array
        for i in range(self.numperiods/2):
            b = a - i*shiftvar - self.samples/self.numperiods #Variable for time 0 of shifted pulse
            formula += N.hstack((tempformula[b:a],tempformula[0:b])) #Starts the pulse at time zero, wraps the remainder
        formula /= self.samples/self.numperiods #Normalizes the pulse to an amplitude of 1
        return (t,formula)
    def run(self, plot = False):
        waveform = self.raisedCos()[1]
        if plot:    
            PL.plot(waveform) 
            PL.show()
        return waveform

class rect:
    def __init__(self, alpha = .75, period = .001, samples = 2000, numperiods = 8):
        self.alpha = alpha
        self.period = period
        self.numperiods = numperiods * 2
        self.samples = samples * numperiods
    def rectangular(self):
        formula = N.ones(self.samples)
        return formula   
    def run(self, plot = False):
        waveform = self.rectangular()
        if plot:    
            PL.plot(waveform) 
            PL.show()
        return waveform

        