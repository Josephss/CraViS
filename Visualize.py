#!/usr/bin/python
import plotly
import csv 
import math
import time, sched
import SimpleHTTPServer
import SocketServer
import os
import numpy as np
import plotly.plotly as py
import RPi.GPIO as GPIO

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plotly.graph_objs import Scatter, Layout, Figure
from plotly import tools

class Handler(FileSystemEventHandler):  
    def process(self, event):
        print event.src_path, event.event_type
        grapher(event.src_path)
    def on_modified(self, event):
        self.process(event)
    def on_created(self, event):
        self.process(event)
        
def hasChanged():
    print("Started monitoring and graphing data files. Press 'Ctrl + C' to terminate.")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path="data/", recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating  ...")
        observer.stop()
    observer.join()
    
    
def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
    
def csvReader(fileName):
    sensorName = filter(str.isdigit,fileName)
    time = []
    temp = []
    f = open(fileName)
    csv_f = csv.reader(f)
    for row in csv_f:
        if(row != -1):
            time.append(row[0])
            if(isFloat(row[1]) == True):
                temp.append(float(row[1]))
    return sensorName, time, temp

#Graph the temperature data from each sensor to their respective HTML file (sensor*.html) using the plotly library
def grapher(fileName):
    trace = []   
    sensor_time_temp = csvReader(fileName)[:]
    trace.append(Scatter(x=sensor_time_temp[1], y=sensor_time_temp[2], name = ("Detector" + str(sensor_time_temp[0]))))
    print("Writing out sensor " + str(sensor_time_temp[0]) + " data ...")
    plotly.offline.plot(trace, filename = ("sensor" + str(sensor_time_temp[0]) + ".html"), auto_open=False, show_link=False)
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
    hasChanged()

if __name__ == "__main__":
    main()
