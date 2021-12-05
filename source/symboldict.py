import modulation
import pulses
import pylab as PL
import scipy as S

class symbolLookupTable:
    def __init__(self, pulsetype = 'raisedCos', modtype = 'bpsk', 
                 samples = 2000, symperiod = .001, alpha = .75, 
                 frequency = 100000):
        self.samples = samples  #Set samples, period & frequency as attributes
        self.symperiod = symperiod
        self.frequency = frequency
        self.modtype = modtype
        self.pulsetype = pulsetype        
        self.symbolDict = {}
        self.modDict = {'bpsk':'bpskMod', 'qpsk':'qpskMod', 'msk':'mskMod'}
        self.pulseDict = {'raisedCos':'raisedCosine', 'rect':'rect'}
        self.alpha = alpha
        entries = 256
        try: 
            self.modDict[self.modtype]
        except: 
            print "Unknown modulation.  Exiting."
            return None
        try: 
            self.pulseDict[self.pulsetype]
        except: 
            print "Unknown pulse type.  Exiting."
            return None
        modvar = getattr(modulation, self.modDict[self.modtype])
        pulsevar = getattr(pulses, self.pulseDict[self.pulsetype])
        modulator = modvar(self.samples, self.symperiod, self.frequency)        
        pulsegen = pulsevar(self.alpha, self.symperiod, self.samples)
        self.pulses = pulsegen.run()       
        for i in range(entries):
            binaryString = self.bin(i)
            symbol = modulator.run(binaryString)
            symbol = symbol * self.pulses
            self.symbolDict[binaryString] = symbol
    def bin(self, decimalValue):
        digits = {'0':'0000','1':'0001','2':'0010','3':'0011',
                  '4':'0100','5':'0101','6':'0110','7':'0111',
                  '8':'1000','9':'1001','A':'1010','B':'1011',
                  'C':'1100','D':'1101','E':'1110','F':'1111'}
        hexStr = "%X" % decimalValue # convert to hexidecimal string
        binStr = ''
        # convert hexidecimal digit to its binary equivalent
        for i in hexStr: binStr += digits[i]
        if len(binStr) == 4:
            binStr = '0000' + binStr
        return binStr
    def plot(self, binaryString):
        PL.subplot(1,2,1)
        PL.plot(self.symbolDict[binaryString])
        fourier = S.fft(self.symbolDict[binaryString])
        PL.subplot(1,2,2)
        PL.semilogy(fourier)
        PL.show()