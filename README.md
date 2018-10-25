CraVis: Cross-Platform Data Visualization System
========
A cross-platform temperature monitoring system for Ge and cryogenic NaI/Csi detectors developed in the radiation detector laboratory.

![CraViS - Room Temperature measurement of our NaI/CsI detector](https://docs.google.com/uc?id=0B9oYjuQx82I8NU5raFp2RVJlRVk "CraViS - Room Temperature measurement of our NaI/CsI detector")

Multiple MAX31865PMB1 hardware setup                |  Single MAX31865PMB1 hardware setup
:-------------------------:|:-------------------------:
![CraViS - Multiple MAX31865PMB1 hardware setup](https://docs.google.com/uc?id=0B9oYjuQx82I8TENiSXdrMFdMU1k "CraViS - Multiple MAX31865PMB1 hardware setup")  | ![CraViS - Single MAX31865PMB1 hardware setup](https://docs.google.com/uc?id=0B9oYjuQx82I8SF9yaTlBOVgyUGs "CraViS - Single MAX31865PMB1 hardware setup")




Look how easy it is to use:
---------------------

1)	Clone or download the entire project to your computer. 
2)	Make sure you have all your temperature sensors are correctly connected to the MAX31865PMB1 board.
3)	Install the Plotly library. 
4)	Run ‘Update.py’ script from the terminal and go to the localhost address.
    

Features
--------
* effortlessly collects data from multiple temperature sensors
* utilizes powerful plotting libraries to graph the output data to a cross-platform interface that is accessible through any web browser enabled device


Installation
------------
Download project folder, install numpy, plotly, watchdog and execute individual py files to bring up a functionality. For example, run MAXPi.py to read from MAX31865, Visualization.py to create plots and serve them to a local browser, etc.

Contribute
----------

- Issue Tracker: github.com/Josephss/CraViS/issues
- Source Code: github.com/Josephss/CraViS

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@marvelouscode.com

License
-------

The project is licensed under the BSD license.
