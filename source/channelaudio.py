"""
File Name: channelaudio.py
Author: Joe Peterson

Purpose:  Convenient way to get audio data from
the open source system (OSS) audio.

Usage:

from channelaudio import *
aiinstance = AudioInterface(sampleRate = 11025)
sample = aiinstance.sampleGrab()

aiinstance.samplePut(sample)

"""
from ossaudiodev import *
from struct import unpack, pack

class AudioInterface:
    def __init__(self, sampleRate, indevice = '/dev/audio', outdevice = '/dev/audio'):
        self.audior = open (indevice,'r')  #Initilize the audio input
        self.audiow = open (outdevice, 'w') #Initialize the audio output
        self.audior.speed(sampleRate)
        self.audiow.speed(sampleRate)
    def sampleGrab(self, numsamples = 1):
        mulawPCM = self.audior.read(numsamples)  #Grab a sample
        mulawPCM = self.bitStream(mulawPCM)  #Convert it to a binary string
        return mulawPCM
    def samplePut(self, mulawPCM):
        mulawPCM = self.unbin(mulawPCM)
        mulawPCM = self.hexStream(mulawPCM) 
        self.audiow.write(mulawPCM)  #Put one sample of the mulawPCM... need to add reverse bitstream convert
    def hexsampleGrab(self, numsamples = 1):
        mulawPCM = self.audior.read(numsamples)    
        return mulawPCM
    def hexsamplePut(self, mulawPCM):
        self.audiow.write(mulawPCM)
    def bitStream(self, mulawPCM):
        #Converts values in mulawPCM string format to binary strings
        decimalValue = unpack('B', mulawPCM)
        binaryString = self.bin(decimalValue)
        return binaryString
    def bin(self, decimalValue):
        digits = {'0':'0000','1':'0001','2':'0010','3':'0011',
                  '4':'0100','5':'0101','6':'0110','7':'0111',
                  '8':'1000','9':'1001','A':'1010','B':'1011',
                  'C':'1100','D':'1101','E':'1110','F':'1111'}
        hexStr = "%X" % decimalValue # convert to hexidecimal string
        binStr = ''
        # convert hexidecimal digit to its binary equivalent
        for i in hexStr: binStr += digits[i]
        return binStr
    def unbin(self, binaryString):
        digits = {'0000':0,'0001':1,'0010':2,'0011':3,
                  '0100':4,'0101':5,'0110':6,'0111':7,
                  '1000':8,'1001':9,'1010':10,'1011':11,
                  '1100':12,'1101':13,'1110':14,'1111':15}
        decimalValue = digits[binaryString[0:4]]*16 + digits[binaryString[4:8]]
        return decimalValue
    def hexStream(self, decimalValue):
        hexValue = pack('B', decimalValue)
        return hexValue