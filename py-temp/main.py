import esp32
import json
import machine
import network
import ntptime
import socket
import time
# import webrepl

import utils

# to read from external temp sensor
from machine import Pin, I2C
import mcp9808


global data
global mcp

def do_connect():
    global data
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(data['ssid'], data['secret'])
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def mcp_read_temp(timer):
    # tf = esp32.raw_temperature()
    # tc = (tf-32.0)/1.8
    # print("T = {0:4d} °F or {1:5.1f} °C".format(tf,tc))
    
    global mcp
    temp_c = mcp.get_temp()
    print("T = ", temp_c, "°C")


if __name__ == "__main__":

    PERIOD_READ_SEC = 10
    USE_TIMER = False
    USE_WIFI = True

    if utils.check_path_exists("/config/"):
        print("Loading configuration...")
        with open('config/configuration.json') as f:
            data = json.load(f)
            ssid = data["ssid"]
            print(ssid)
    else:
        print("ERR: config folder not present")

    # set the blue led
    blue_led = machine.Pin(2, machine.Pin.OUT)

    # set I2C communication with temperature sensor (mcp9808)
    i2c = I2C(1,scl=Pin(22), sda=Pin(21), freq=100000)
    mcp = mcp9808.MCP9808(i2c)

    print("Luca")

    if (USE_TIMER):
        ''' I prefer not to use this when debugging '''
        timer=machine.Timer(0)
        timer.init(period=PERIOD_READ_SEC*1000, mode=machine.Timer.PERIODIC, callback=mcp_read_temp)

    if (USE_WIFI):
        do_connect()
        ntptime.settime()
    
    # main loop (remove it and use timer)
    while (True):
        blue_led.on()
        # temp_C = mcp.get_temp()
        temp_C = 10
        msg = time.localtime(), ": T = ", temp_C, "°C"
        print(msg)
        blue_led.off()
        time.sleep(PERIOD_READ_SEC)

    # import webrepl_setup

