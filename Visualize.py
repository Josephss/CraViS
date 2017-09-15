#!/usr/bin/python
import plotly
import csv 
import math
import time, sched
import SimpleHTTPServer
import SocketServer

import numpy as np
import plotly.plotly as py
import RPi.GPIO as GPIO

from plotly.graph_objs import Scatter, Layout, Figure
from plotly import tools


def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
    
def csvReader(fileNameArr):
    n = len(fileNameArr) 
    #Store the time and temp values in a multi-dimentional array
    time_temp = [[] for index in range(0,n*2)]
    for i in range(n):
        #read in the CSV and store it in a huge array
        f = open(fileNameArr[i])
        csv_f = csv.reader(f)
        for row in csv_f:
            if(row != -1):
                if(i>=1):
                    time_temp[i+i].append(row[0])
                    if(isFloat(row[1]) == True):
                        time_temp[i+i+1].append(float(row[1]))
                else:
                    time_temp[i].append(row[0])
                    if(isFloat(row[1]) == True):
                        time_temp[i+1].append(float(row[1]))
    return time_temp

#Graph the temperature data to an HTML file (temperature.html) using the plotly library
def grapher(rate):
    looper = True
    while(looper):
            try:
                time_temp = csvReader(['sensor01.csv','sensor02.csv','sensor03.csv','sensor04.csv'])[:]
                n = len(time_temp)
                traces_arr = [[] for index in range(0,n/2)]
                for val in range(val/2):
                	if(val>=1):
                		tempVal = trace+str(val) = Scatter(x=time_temp[val+val], y=time_temp[val+val+1], name ="Detector " + str(val+1))
                		traces_arr[val].append(tempVal)
                	else:
                		tempVal = trace+str(val) = Scatter(x=time_temp[val], y=time_temp[val+1], name ="Detector " + str(val+1))
               			traces_arr[val].append(tempVal)
                
                for i in range(val/2):
                	fig = []
                	fig.append(traces_arr[i])
                	plotly.offline.plot(fig, filename = "sensor" +str(i+1) + ".html", auto_open=False, show_link=False)
                	fig[:]
                time.sleep(rate)
                traces_arr[:]
            except KeyboardInterrupt:
                print("Terminating graphing ...")
                looper = False
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

def main():
    grapher(5)

if __name__ == "__main__":
    main()
