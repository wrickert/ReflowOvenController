import rainbowPiano
#rainbowPiano.keys()

from machine import Pin,I2C,Timer
from PDM import PDM
from PID import PID
from MCP9600 import MCP9600
from SSD1306 import SSD1306_I2C
import micropython
import ntptime
import utime
import sys

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

"""
def __init__():
    global seconds
    global stage
    seconds = 0
    stage = 0
"""

def get_temp():
    global tc
    #return tc.fir.get_value()*0.25
    return tc.read()

def load():
    pdm.tim.deinit()

pid = PID(get_temp,pdm.set_output)

# This function runs the pid and controls the display
def run(point):
    prev_t = ''
    global seconds
    while True:#sw_state:
        profile()
        temp= tc.read()
        pid.set_point = point 
        pid.update()
        #avg_temp = tc.fir.get_value()*0.25
        avg_temp = tc.read()
        avg_temp = str(avg_temp)
        t =  "Temp     " + avg_temp + "F\r\r"
        #t =     "Temperature  " + avg_temp[:4] + "C\r\r"
        u =  "Setpoint " + str(point) + "F\r\r"
        v =  "Output   "+str(pid.output)[:6]+ "%\r\r\r"
        w =  "P: " + str(pid.P_value)[:5] + "  I: "+str(pid.I_value)[:5]+"\r"


        if t!=prev_t:
            print(t)
            print(u)
            print(v)
            print()
            oled.fill(0)
            
            oled.text(str(utime.localtime()[3]-5)+":"+str(utime.localtime()[4]),0,0)
            oled.text(t,0,20)
            oled.text(u,0,30)
            oled.text(v,0,40)
            oled.text(str(seconds),100,0)
            oled.show()
            prev_t = t
        utime.sleep_ms(1000)

# This function follows the reflow curve of SMD291AX250T3 smt paste
def reflow():
    timeStart = utime.ticks_ms()
    stage = 1
    run(target[stage])


    """
    reflowTimer = Timer(-1)
    print("in reflow")
    reflowTimer.init(period=1000, mode=Timer.PERIODIC, callback=profile())   
    """

target = [0,302,347,423,480,423,0]
#target = [0,200,300,361,455,361,0]
time =   [0,90,180,210,240,270,260]
#time =   [0,90,120,150,210,240,260]
timeStart = 0 
seconds = 0
stage = 0

def profile():
    global seconds 
    global target
    global stage
    seconds = (utime.ticks_diff(utime.ticks_ms(),timeStart)/1000)
    #seconds = seconds +1
    print("             Seconds are " + str(seconds))
    if stage == 6:
        print("Done!")
        exit()
    if tc.read() >= target[stage] and seconds >= time[stage]:
        stage = stage + 1
        print("************Moving to stage "+ str(stage) + " at tempature "+str(target[stage])+"**********")
        run(target[stage])
       
def exit():
    #TODO play tone here
    #reflowTimer.deinit() 
    rainbowPiano.setTone(4)
    utime.sleep_ms(500) 
    rainbowPiano.setTone(0)
    pdm.pout.value(0)
    sys.exit()
    
