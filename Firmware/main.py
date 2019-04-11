#import rainbowPiano

#rainbowPiano.keys()

from machine import Pin,I2C
from PDM import PDM
from PID import PID
from MCP9600 import MCP9600
from SSD1306 import SSD1306_I2C
import micropython
import ntptime
import utime

micropython.alloc_emergency_exception_buf(100)

pdm = PDM()
tc = MCP9600()

oled = SSD1306_I2C(128,64,tc.i2c)

oled.text(sta_if.ifconfig()[0],0,0)
oled.show()

ntptime.settime()
oled.text(str(utime.localtime()[3]-5)+":"+str(utime.localtime()[4]),0,20)
oled.show()

pdm.set_output(0.7)

def get_temp():
    global tc
    #return tc.fir.get_value()*0.25
    return tc.read()

def load():
    pdm.tim.deinit()

pid = PID(get_temp,pdm.set_output)

def run(point):
    prev_t = ''
    while True:#sw_state:
        temp= tc.read()
        pid.set_point = point 
        pid.update()
        #avg_temp = tc.fir.get_value()*0.25
        avg_temp = tc.read()
        avg_temp = str(avg_temp)
        t =     "Temperature  " + avg_temp + "C\r\r"
        #t =     "Temperature  " + avg_temp[:4] + "C\r\r"
        t =  t+ "Setpoint     " + str(point) + "C\r\r"
        t =  t+ "Output       "+str(pid.output)[:6]+ "%\r\r\r"
        t =  t+ "P: " + str(pid.P_value)[:5] + "  I: "+str(pid.I_value)[:5]+"\r"


        if t!=prev_t:
            print(t)
            oled.fill(0)
            oled.text(str(utime.localtime()[3]-5)+":"+str(utime.localtime()[4]),0,0)
            oled.text(t,0,20)
            prev_t = t
        utime.sleep_ms(50)

