#!/usr/bin/env python

import pylab as PL
import numpy as N
import scipy as S
from modulation import *
from pulses import *

qmd = qpskMod(samples = 200, frequency = 50000) 
qmdarray = qmd.run('10010010100010101000101110110111010001010000011101011001001')

bmd = bpskMod(samples = 200, frequency = 50000) 
bmdarray = bmd.run('10010010100010101000101110110111010001010000011101011001001')

mmd = mskMod(samples = 200, frequency = 50000)
mmdarray = mmd.run('10010010100010101000101110110111010001010000011101011001001')

bins = pow(2, 10)
sampfreq = 200000

PL.psd(qmdarray, NFFT = bins, Fs = sampfreq, label = 'QPSK')
PL.psd(bmdarray, NFFT = bins, Fs = sampfreq, label = 'BPSK')
PL.psd(mmdarray, NFFT = bins, Fs = sampfreq, label = '2-MSK')

PL.legend(('QPSK', 'BPSK', '2-MSK'), loc='upper right')
PL.show()


