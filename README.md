# Baby Tracker App
A locally hosted Python web app to track and visualize baby's eating, sleeping, and potty events. 


## Table of Contents
* [General info](#general-info)
* [Dependencies](#dependencies)
* [Installation](#installation)


## General Info
I built this web app to help me and my wife track our newborn's sleep, eating, and potty patterns through the days, weeks, and months. It has been surprisingly helpful to see poo trends, remember how long it's been since baby's last nap, and remember which side she fed on last. The web app is built using [Plotly Dash](https://plotly.com/dash/) which is a great open source tool for quickly creating web apps with nothing but Python!

There are 3 tabs in the app: 
* The "Input" tab is where you input details about an event. This tab is designed to have persistence within a browser session to allow you to record a start time, put down your phone, and pick it up later to submit the event. This only works if your leave the browser open in the background. 
<p align="center">
<img src="https://github.com/jhthompson12/Baby_Tracker_App/blob/master/images/input_tab.png?raw=true" width="35%" align="center">
</p>

* The "History" tab shows an editable table with the last 200 events. Here events can be modified or deleted. If you want to see more or less events on this page you can easily change this in `main.py`.
<p align="center">
<img src="https://github.com/jhthompson12/Baby_Tracker_App/blob/master/images/history_tab.png?raw=true" width="35%" align="center">
</p>

* The "Analytics" tab currently shows an interactive Gantt chart of the last 7 days of events, but you could add tons of other things here with a little bit of editing. 
<p align="center">
<img src="https://github.com/jhthompson12/Baby_Tracker_App/blob/master/images/analytics_tab.png?raw=true" width="35%" align="center">
</p>


## Dependencies
### Hardware
* Raspberry Pi 3 or 4: This project is designed to run on a dedicated GNU/Linux machine that is always on and connected to your Local Area Network (LAN). I think most aspects of the app would run quickly on pretty much any Raspberry Pi, but some things, like the loading of the "Analytics" tab can be very slow.
    * With some minor adjustments this could be run on pretty much any OS, but this project will only describe how to set it up on GNU/Linux

### Software
* Python 3.6 or higher and mostly these libraries:
    * [virtualenv](https://pypi.org/project/virtualenv)
    * [dash](https://plotly.com/dash/) 
    * [pandas](https://pandas.pydata.org/)
    * Other library dependencies covered in the [requirements.txt](https://github.com/jhthompson12/Baby_Tracker_App/blob/master/requirements.txt)


## Installation
### Set up the Raspberry Pi Server
* Setup the Raspberry Pi on your LAN. Connect to the Pi either directly with a monitor, mouse, and keyboard or through an SSH session. Open the Pi's terminal if **not** connected with SSH. 

### Clone this project
* Change directory (cd) into the directory where you want to clone this project. This example will clone the directory into the `/home/pi` (~) directory.
        
        cd ~
        git clone https://github.com/jhthompson12/Baby_Tracker_App.git
* Then cd into the project directory
        
        cd Baby_Tracker_App


### Create a Python Virtual Environment for this project
* The Pi should already have Python 3 installed, so install the virtualenv library
        
        python3 -m pip install virtualenv
* Create a virtualenv for our project

        python3 -m virtualenv env
* Install the required libraries

        ./env/bin/pip install -r requirements.txt
        
### Create a service for running our app
* Move the `baby_tracker.service` file to `/etc/systemd/system`

        sudo mv baby_tracker.service /etc/systemd/system
* Start the service to get our app up and running
        
        sudo systemctl start baby_tracker.service
* If you want the service to start whenever the Raspberry Pi boots (like after a power failure)

        sudo systemctl enable baby_tracker.service
        
Now on any device that is connected to the same LAN as the Raspberry Pi, you should be able to open a browser and navigate to `http://Your_Pi's_IP_Address:8050` and see the "Input" tab. Bookmark this URL and / or add a shortcut to it on your phone's home screen and it will feel kinda like it is running a native app! 
