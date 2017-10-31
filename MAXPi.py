#!/usr/bin/python

import csv 
import math
import time, sched
import urllib
import os.path
import numpy as np
import plotly.plotly as py
import RPi.GPIO as GPIO

from datetime import datetime
from MAX31865 import MAX31865, MAX31865Error

def fileWrite(time, data, fileName):
    completePath = os.path.join("data/",fileName + '.csv')
    with open(completePath, 'a') as fl:
        writer = csv.writer(fl)
        writer.writerow((time, data)) #TODO: trim temperature value to ($$.$$)
        fl.close()
    return

# Inputs an array of cx_pins locations of ADC's
# Outputs raw data, measured resistance and temperature reading of the PT-100
def getTemperature(cs_arr):
 
    cs_pins = cs_arr #[8] # 25, 24
    clock_pin = 11
    data_in_pin = 9
    data_out_pin = 10
    tempeature = []

    rtds = []
    address = int(0x80)    # RTD control register, see datasheet for details
    data =  int(0xC2)      # RTD control register data, see datasheet for details
    for cs_pin in cs_pins:
        rtds.append(MAX31865(cs_pin, clock_pin, data_in_pin, data_out_pin, address, data))  
    for rtd in rtds:        
        rtd.write()

    for rtd in rtds:
        code = rtd.get_data()
        data = rtd.convert(code)
        temperature = data.split()
    return temperature
    
# Takes in an array of MAX31865PMB1 pin 6 locations and saves their temperature output to individual CSV files
def aquire(pin, rate):
    print("Saving data locally ... Press Ctrl + C to terminate.")
    looper = True
    while(looper):
            try:
                n = len(pin) # number of pins
                temperature_data_arr = []
                for i in range(n): # collect the temperature data in an array
                    temperature_data_arr.append(getTemperature(pin[i])[2])
                for j in range(n): # save the collected data to individual CSV files
                    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    fileWrite(currentTime, temperature_data_arr[j], 'sensor0'+str(j+1))                
                time.sleep(rate)
                del temperature_data_arr[:] # flush out old data
            except KeyboardInterrupt:
                print("Terminating ...")
                GPIO.cleanup()
                looper = False
    return
	
#Check internet connection:     
def connected(host='http://google.com'):
    try:
        urllib.urlopen(host)
        return True
    except:
        return False
    
def main():
    aquire([[8],[4], [25], [24]], 2)

if __name__ == "__main__":
    main()
