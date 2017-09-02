#!/usr/bin/python
import plotly
import csv 
import math
import time, sched
import SimpleHTTPServer
import SocketServer
import threading

import numpy as np
import plotly.plotly as py
import RPi.GPIO as GPIO

from plotly.graph_objs import Scatter, Layout, Figure
from plotly import tools
from datetime import datetime
from MAX31865 import MAX31865, MAX31865Error


#Store the time and temp values in separate arrays
Time = []
temp = []

def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
    
def csvReader(fileName):
    #flush out the existing data of Time and temp before updating the updated data to the html
    del Time[:]
    del temp[:]
    #read in the CSV and store it in a huge array
    f = open(fileName)
    csv_f = csv.reader(f)
    for row in csv_f:
        if(row != -1):
            Time.append(row[0])
            if(isFloat(row[1]) == True):
                temp.append(float(row[1]))
    return

#Graph the temperature data to an HTML file (temperature.html) using the plotly library
def grapher(rate):
    looper = True
    while(looper):
            try:
                csvReader('data.csv')
                trace0 = Scatter(x=Time, y=temp, name ="Detector 1")
                trace1 = Scatter(x=Time, y=temp, name ="Detector 2 ")
                fig = tools.make_subplots(rows=2, cols=1)
                fig.append_trace(trace0, 1, 1)
                fig.append_trace(trace1, 2, 1)
                plotly.offline.plot(fig, filename = "temperature" + ".html", auto_open=False, show_link=False)
                time.sleep(rate)
            except KeyboardInterrupt:
                print("Terminating graphing ...")
                looper = False
    return

def fileWrite(time, data, fileName):
    #np.savetxt('data.csv', (str(time), str(data)), delimiter=',')
    with open(fileName + '.csv', 'a') as fl:
        writer = csv.writer(fl)
        writer.writerow((time, data)) #TODO: trim temperature value to ($$.$$)
        fl.close()
    return

#Config and start the python server to host the files from the directory
def server():
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.webapp': 'application/x-web-app-manifest+json',
    });
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    
    print ("Serving at port:", PORT)
    httpd.serve_forever()
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

def offilne(pin, rate):

    print("Saving data locally ... Press Ctrl + C to terminate.")
    
    looper = True
    while(looper):
            try:
                temp1_data = getTemperature(pin[0])
                temp = temp1_data[2]

                temp2_data = getTemperature(pin[1])
                temp2 = temp2_data[2]

                temp3_data = getTemperature(pin[2])
                temp3 = temp3_data[2]
                
                temp4_data = getTemperature(pin[3])
                temp4 = temp4_data[2]

                currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')            
                
                fileWrite(currentTime, temp, 'sensor01')
                fileWrite(currentTime, temp2, 'sensor02')
                fileWrite(currentTime, temp3, 'sensor03')
                fileWrite(currentTime, temp4, 'sensor04')
                time.sleep(rate)
            except KeyboardInterrupt:
                print("Terminating ...")
                GPIO.cleanup()
                looper = False
    return

def streamer(pin, rate):

    print("Streaming ... Press Ctrl + C to terminate.")
    username = 'marvlouscoder'
    api_key = 'lYGlKUdZ1Digw9b6cF9H'
    stream_token = '6w2ya7ee7l'
    stream_token_2 = '4qkr510mpn'
    stream_token_3 = 'kk30tc3m92'
    stream_token_4 = '8mamxc4nk8'

    
    py.sign_in(username, api_key)

    trace1 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token,
            maxpoints=100
        ),
        name = 'Sensor 1'
    )

    trace2 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token_2,
            maxpoints = 100
            ),
        name = 'Sensor 2'
    )
    trace3 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token_3,
            maxpoints=100
        ),
        name = 'Sensor 3'
    )

    trace4 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token_4,
            maxpoints = 100
            ),
        name = 'Sensor 4'
    )
    
    layout = Layout(
        title='Detector 01 Temperature Data',
        xaxis=dict(
            title='Time',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Temperature data in Celcius',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
        
    )
    fig = Figure(data=[trace1, trace2, trace3, trace4], layout=layout)

    print (py.plot(fig, filename='Detector 01 and 02 Temperature Data'))


    
    stream = py.Stream(stream_token)
    stream_2 = py.Stream(stream_token_2)
    stream_3 = py.Stream(stream_token_3)
    stream_4 = py.Stream(stream_token_4)
    stream.open()
    stream_2.open()
    stream_3.open()
    stream_4.open()
    Time = 0
    i = 0
    
    looper = True
    while(looper):
            try:
                temp1_data = getTemperature(pin[0])
                temp = temp1_data[2]

                temp2_data = getTemperature(pin[1])
                temp2 = temp2_data[2]

                temp3_data = getTemperature(pin[2])
                temp3 = temp3_data[2]
                
                temp4_data = getTemperature(pin[3])
                temp4 = temp4_data[2]

                currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                stream.write({'x': currentTime, 'y': temp})
                stream_2.write({'x': currentTime, 'y': temp2})
                stream_3.write({'x': currentTime, 'y': temp3})
                stream_4.write({'x': currentTime, 'y': temp4})

                i += 1
                
                stream.close()
                stream_2.close()
                stream_3.close()
                stream_4.close()                
                time.sleep(rate)
                stream.close()
                stream_2.close()
                stream_3.close()
                stream_4.close()
                
                #statusCheck(temp, temp2)
                
                fileWrite(currentTime, temp, 'sensor01')
                fileWrite(currentTime, temp2, 'sensor02')
                fileWrite(currentTime, temp3, 'sensor03')
                fileWrite(currentTime, temp4, 'sensor04')
            except KeyboardInterrupt:
                print("Terminating streaming ...")
                GPIO.cleanup()
                looper = False
	return
	
def terminate():
    print("Terminating ..")
    for thread in Thread.enumerate():
        if(thread.isAlive()):
            thread._Thread_stop()

def statusCheck(temp1, temp2):
    if(temp1 > 28 or temp2 > 28):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(20, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(20, GPIO.LOW)
    GPIO.cleanup()

    
def main():
	#TODO: check internet connection
	#if yes, call streamer. Else, call offline
    offline([[8],[24], [25], [4]], 2)

if __name__ == "__main__":
    main()
