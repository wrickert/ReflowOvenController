# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import network
#esp.osdebug(None)
import webrepl

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('Trenzalore', 'TheKnightsWhoSayNi')
    webrepl.start()
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
