def raisedCosine(alpha = .99, period = .001, samples = 16000, numperiods = 16):
    t = N.arange(samples) * period/samples * numperiods  #Generate the time array
    t = t - period * numperiods / 2 #Shift the array to the left to center the pulse on time = 0
    term1 = N.sinc(t/period)/period  #The next four lines calculate the dependent variable
    term2 = N.cos((t * alpha * S.pi)/period)
    term3 = 1 - pow((4 * alpha * t) / (2 * period),2)
    tempformula = term1 * term2 / term3
    t = t + period * numperiods / 2  #Shift the pulse back over so it's causal
    formula = N.zeros(len(t)) #Create a new array to hold a series of pulses
    shiftvar = 2*samples/numperiods #Define shift variable to move pulses in time
    a = len(t) #Variable for the upper index limit of the pulse array
    for i in range(numperiods/2):
        b = a - i*shiftvar - samples/numperiods #Variable for time 0 of shifted pulse
        formula += N.hstack((tempformula[b:a],tempformula[0:b])) #Starts the pulse at time zero, wraps the remainder
    formula /= samples/numperiods #Normalizes the pulse to an amplitude of 1
    #PL.plot(t,formula) 
    #PL.show()
    return (t,formula)

def bpskMod(period = .001, samples = 1000, binary = '1', amplitude = 1, frequency = 10000, numperiods = 1):
    lookupdict = {'0':1, '1':0}
    symbol = lookupdict[binary]
    t = N.arange(samples) * period/samples  #Generate the time array
    formula = amplitude * N.cos(2 * S.pi * frequency * t + symbol * S.pi) #This line calculates the dependent variable 
    formula = stackarrays(formula, numperiods)
    #PL.plot(formula)
    #PL.show()
    return(t, formula)

def qpskMod(period = .001, samples = 1000, binary = '00', amplitude = 1, frequency = 10000, numperiods = 1):
    lookupdict = {'00':0, '01':1, '10':2, '11':3}
    symbol = lookupdict[binary]
    t = N.arange(samples) * period/samples #Generate the time array
    formula = amplitude * N.cos(2 * S.pi * frequency * t + symbol * S.pi/2)  #This line calculates the dependent variable 
    formula = stackarrays(formula, numperiods)
    #PL.plot(formula)
    #PL.show()
    return(t, formula)

def stackarrays(array, numstack): #Replicates and appends an array numstack times
    modlist = []
    for i in range(numstack):
        modlist.append(array)
    newarray = N.hstack(tuple(modlist))
    return newarray

#This main function records a bit of input and then plays it back
def main():
    
    #cu = CursesUser() #Instance of CursesUser
    #AE.register(cu.shutdown)
    audio = AudioInterface() #Instance of AudioInterface
    audioarray = N.zeros(50000)
    audio.audioRead()
    audio.audioWrite()
    print "Recording..."
    for i in range(len(audioarray)):
        thissample = audio.unbin(audio.audioSampleGrab()) #put integers in the array       
        audioarray[i] = thissample
    print "Playing..."
    for i in range(len(audioarray)):
        audio.audioSamplePut(audio.hexStream(audioarray[i])) #pass the output to audio
    exit()    

#This main function just passes the latest sample to the output -- there's a bit of a delay
def main():
    
    #cu = CursesUser() #Instance of CursesUser
    #AE.register(cu.shutdown)
    audio = AudioInterface() #Instance of AudioInterface
    audioarray = N.zeros(50000)
    audio.audioRead()
    audio.audioWrite()
    while(1):
        thissample = audio.unbin(audio.audioSampleGrab()) #put integers in the array       
        audio.audioSamplePut(audio.hexStream(thissample)) #pass the output to audio
    exit() 
    
class symboldict:
    def __init__(self, pulsetype = 'raisedCos', modtype = 'bpsk', 
                 samples = 2000, symperiod = .001, 
                 frequency = 100000):
        self.samples = samples  #Set samples, period & frequency as attributes
        self.symperiod = symperiod
        self.frequency = frequency
        self.modtype = modtype
        self.pulsetype = pulsetype        
        self.symbolDict = {}
        self.modDict = {'bpsk':'bpskMod', 'qpsk':'qpskMod', 'msk':'mskMod'}
        self.pulseDict = {'raisedCos':'raisedCosine', 'rect':'rect')
        entries = 256
        try: 
            self.modDict[self.modulation]
        except: 
            print "Unknown modulation.  Exiting."
            exit()       
        try: 
            self.pulseDict[self.pulsetype]
        except: 
            print "Unknown pulse type.  Exiting."
            exit()
        modvar = modulation.getattr(modulation, self.modDict[self.modtype]
        modulator = modvar(self.samples, self.symperiod, self.frequency)
        for i in range(entries):
            binaryString = self.bin(i)
            symbol = modulator.run(binaryString)
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
            
if len(psdarray) > len(randseq):
    randseq = N.hstack((randseq, N.zeros(len(psdarray) - len(randseq))))
elif len(psdarray) < len(randseq):
    randseq = randseq[1:len(psdarray)]
        
outfile = open('test.out', 'w')
audio = AudioInterface(4000) #Instance of AudioInterface
print "Working..."    
for i in range(10000):
    thissample = audio.hexsampleGrab(1) #put integers in the array 
    audio.hexsamplePut(thissample) #pass the output to audio
    outfile.write(str(clock()))
outfile.close()

self.Qin = Queue.Queue()
self.Qout = Queue.Queue() 

new_thread = threading.Thread(target = self.putAudioinQueue)
        new_thread.start()
        new_thread = threading.Thread(target = self.putAudiofromQueue)
        new_thread.start()    
        new_thread = threading.Thread(target = self.passAudioThruChannel)
        new_thread.start()
        
def putAudioinQueue(self):
    while True:        
        thissample = self.audio.sampleGrab()
        print thissample    
        self.Qin.put(thissample)
def putAudiofromQueue(self):
    while True:            
        thissample = self.Qout.get()
        self.audio.samplePut(thissample)