#!/usr/bin/env python

"""
File: SymbolDict Timing Test
"""

from modulation import *
from symboldict import *
import numpy as N
import pylab as PL
from time import *

qm = bpskMod(samples = 2000)
bm = qpskMod(samples = 2000)
mm = mskMod(samples = 2000)

sltbm = symbolLookupTable('rect', 'bpsk', 2000, .001, 1, 10000).symbolDict
sltqm = symbolLookupTable('rect', 'qpsk', 2000, .001, 1, 10000).symbolDict
sltmm = symbolLookupTable('rect', 'msk', 2000, .001, 1, 10000).symbolDict

timematrix = []
timematrix.append(['QPSK Method', clock()])

testreps = 100000

for i in range(testreps):
    testvar = qm.run('00011011')

timematrix[0].append(clock())

timematrix.append(['BPSK Method', clock()])

for i in range(testreps):
    testvar = bm.run('00011011')

timematrix[1].append(clock())

timematrix.append(['2-MSK Method', clock()])

for i in range(testreps):
    testvar = mm.run('00011011')

timematrix[2].append(clock())

timematrix.append(['BPSK SLT', clock()])

for i in range(testreps):
    testvar = sltbm['00011011']

timematrix[3].append(clock())

timematrix.append(['QPSK SLT', clock()])

for i in range(testreps):
    testvar = sltqm['00011011']

timematrix[4].append(clock())

timematrix.append(['2-MSK SLT', clock()])

for i in range(testreps):
    testvar = sltmm['00011011']

timematrix[5].append(clock())

leftarray = N.arange(6)
heightarray = N.zeros(6)
namelist = []

for i in range(6):
    heightarray[i] = (timematrix[i][2]-timematrix[i][1])/float(testreps)
    namelist.append(timematrix[i][0])
    print timematrix[i][0]    
    print heightarray[i]

PL.subplot(1,2,1)
PL.bar(leftarray[0:3], heightarray[0:3])
PL.xticks(N.arange(3)+.5, (namelist[0], namelist[1], namelist[2]))
PL.title('Modulation Module Run Methods')
PL.subplot(1,2,2)
PL.bar(leftarray[0:3], heightarray[3:6])
PL.xticks(N.arange(3)+.5, (namelist[3], namelist[4], namelist[5]))
PL.title('Symbol Lookup Table')
PL.show()

