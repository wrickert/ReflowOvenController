from machine import Pin,I2C

def temp_f(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16
    f = (temp * (9/5)) + 32
    return f


