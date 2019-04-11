# Pulse Density Modulator 

from machine import Pin,Timer
import time

class PDM():
    def __init__(self,pout=19,freq=20):
        """
        :param pout: output pin nr
        :param tim:  timer number
        :param freq: frequency of the bitstream
        """
        self.max = 2**24-1#2**31-1 crashes with larger ints? 24bit resolution is fine enough ;)

        self.pout = Pin(pout, Pin.OUT)

        self.err = 0 # error accumulator
        self.output = 0

        self.freq = freq

        # -1 seems to be the only timer on esp32
        self.tim = Timer(-1)
        self.tim.init(mode=Timer.PERIODIC, period=freq,callback=lambda t: self.call_me())

    def set_output(self,out):
        """
        :param out: desired output as a value between 0 and 1
        """
        print ('setting output to '+str(out))
        self.tim.deinit()

        self.output = int(self.max*out)

        self.tim.init(mode=Timer.PERIODIC, period=self.freq,callback=lambda t: self.call_me())

    def call_me(self):
        if self.err >= 0:
            self.pout.value(0)
            self.err -= self.output
        else:
            self.pout.value(1)
            self.err += self.max
            self.err -= self.output
