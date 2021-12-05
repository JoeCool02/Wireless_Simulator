#!/usr/bin/env python

from rayleighfade import *
from modulation import *
import pylab as PL
qm = qpskMod(samples = 2000)
signal = qm.run('10001001')
rf = rayleighFade(maxdoppler = 100, seqlength = 5000)
rf.run(signal, plot = True)

