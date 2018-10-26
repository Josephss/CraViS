#!/usr/bin/python

import csv 
import math
import time, sched
import os, subprocess
import ctypes as ct
import numpy as np
import sys

from threading import Thread
from datetime import datetime
from multiprocessing import Process

#call the MCC 1608FS-PLUS DAQ driver from the shared object file
ct.cdll.LoadLibrary('libmccusb.so')
Libusb = ct.CDLL('libmccusb.so')

R0 = 100.0
A = 0.0039083
B = -5.775e-7
C = -4.183e-12
I = 0.0168 

def voltage_to_temperature(voltage):
    R_t = voltage / I
    D = (R_t / R0 - 1) / B
    E = A / 2 / B
    E_2 = math.pow(E, 2)
    T_cnvt = -E - math.sqrt(E_2 + D)
    T_del = 1
    if T_cnvt < 0:
        t_out3 = T_cnvt * T_cnvt * T_cnvt
        F_t = C * t_out3 * (T_cnvt - 100)
        while T_del > 0.00001:
            D_A = 2 * B * T_cnvt
            D_B = 4 * C * math.pow(T_cnvt, 2) * (T_cnvt - 75)
            D_t = A + D_A + D_B
            T_del = -F_t / D_t
            T_cnvt = T_cnvt + T_del
            F = 1 + A * T_cnvt + B * math.pow(T_cnvt, 2) + C \
                * math.pow(T_cnvt, 3) * (T_cnvt - 100)
            F_t = R_t / R0 - F
    return np.round(T_cnvt)

def volts_USB1608FS_Plus(value, range):
    if (range == 0):
        volt = (value - 0x8000)*10.0/32768
    elif (range == 1):
        volt = (value - 0x8000)*5.0/32768
    elif (range == 3):
        volt = (value - 0x8000)*2.0/32768
    elif (range == 5):
        volt = (value - 0x8000)*1.0/32768
    return volt

def aquire(channel, range, rate):
    USB1608FS_PLUS_PID=0x00ea

    ret = Libusb.libusb_init(0)
    udev = Libusb.usb_device_find_USB_MCC(USB1608FS_PLUS_PID, 0)

    if(ret < 0):
        print("usb_device_find_USB_MCC: Failed to initialize libusb")
        exit(1)

    if(udev):
        print("Found a USB 1608FS-Plus!")
    else:
        print("USB 1608FS-Plus is not detected (or is currently being used by another program)!")
        return 0

    print("Collecting date from the DAQ from channel: " + str(channel) + ", range: " + str(range) + " at the rate of: " + str(rate) + " seconds.")
    #Take in the data from the text file (2D matrix by default) and convert it to 8x8x2
    a = np.loadtxt('table_AIN.txt')
    table_AIN = a.reshape((8,8,2))
    while True:
        value = Libusb.usbAIn_USB1608FS_Plus(udev, channel, range)
        value = value * table_AIN[range][channel][0] + table_AIN[range][channel][1]
        value = volts_USB1608FS_Plus(value, range)
        #emf.append(value)
        temp = voltage_to_temperature(value)
        Time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        fileWrite(Time, temp, "sensor_"+ channel)
        time.sleep(rate)
  
    return

def fileWrite(time, data, filename):
    with open(filename + '.csv', 'a') as fl:
        writer = csv.writer(fl)
        writer.writerow((time, data)) #TODO: trim temperature value to ($$.$$)
        fl.close()
    return

def terminate():
    print("Terminating ..")
    for thread in Thread.enumerate():
        if(thread.isAlive()):
            thread._Thread_stop()
    
def main():
    try:
        Collect = Thread(target = aquire, args=(0,3,2,)) # aquire the data from the DAQ
        #Collect.setDaemon(True)
        Collect.start()
    except KeyboardInterrupt:
        terminate() # terminate the threads       
  
if __name__ == "__main__":
    main()
