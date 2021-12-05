#! /usr/bin/env python

class CalcSINR():
    def get_frequencyReuseFactor(self):
        i = float(raw_input("What is i? "))
        j = float(raw_input("What is j? "))
        N = pow(i, 2) + pow(j, 2) + i * j
        print ("The Frequency Reuse Factor is %f" % N)
        return N
    def calcSINR(self):
        coChannelReuseRatio = sqrt(3*self.get_frequencyReuseFactor())
        term1 = 2 * pow(coChannelReuseRatio - 1, -4)
        term2 = 2 * pow(coChannelReuseRatio + 1, -4)
        term3 = 2 * pow(coChannelReuseRatio, -4)
        SIR = 1 / (term1 + term2 + term3)
        SIRdB = 10 * log10(SIR)
        print ("The Co-Channel Reuse Ratio is %f" % coChannelReuseRatio)
        print ("The SIR is %f" % SIR)
        print ("The SIR in decibels is %f" % SIRdB)
        OneTwentySIRdb = 10 * log10(SIR * 3)
        print ("The SIR for 120 degree sectoring in decibels is %f" % OneTwentySIRdb)
        SixtySIRdb = 10 * log10 (SIR * 6)
        print ("The SIR for 60 degree sectoring in decibels is %f" % SixtySIRdb)
 
if __name__ == "__main__":
    from math import *
    calculation=CalcSINR()
    calculation.calcSINR()
    exit()

