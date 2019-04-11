from FIR import FIR
from machine import Pin,I2C
import time

class MCP9600():
    def __init__(self,sda_pin=5,scl_pin=18):
        self.i2c = I2C(sda=Pin(sda_pin), scl=Pin(scl_pin), freq=100000)

        self.fir = FIR(window_size=16,div=8)

        self.lastReadTime = 0
        self.lastReadRoomTemp = 0
        self.lastReadTCTemp = 0
        self.fault = 0
        

    def read(self):
        if time.ticks_ms() - self.lastReadTime > 100:
            tc_temp = 0

            # TODO should add sign check
            data = self.i2c.readfrom_mem(96,0,2)
            value = (data[0] << 8) | data[1]
            
            # Temp in C 
            temp = (value & 0xFFF) / 16
    
            # Temp in F 
            f = (temp * (9/5)) + 32

            self.lastReadTime = time.ticks_ms()
            self.lastReadTCTemp = temp  

            # TODO change this back to float for better precision
            self.fir.push(int(temp))
            return temp
        else:
            return self.lastReadTCTemp 
