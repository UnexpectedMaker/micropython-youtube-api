# micropython-youtube-api
A MicroPython based Youtube API wrapper library and example code that allows you to connect to the Google Apps API backend to obtain channel stats for aa YouTube channel.

## Setting up the config.json

The config.json file contains entried you will need to fill in for the following items:
* ssid - Your Wifi network SSID
* ssid_password - Your WiFi router password
* appkeyid - Your API kety from Google (See below on how to opbtain one)
* channelid - Your YouTube Channel ID


## Installing

Download the repositry and copy the following files to your ESP8266 or ESP32 Development board running the latest mainline  MicroPython firmware

* micropython_youtube_api.py
* config.json 
* urequests.py
* Optional: grab_stats.py from examples folder


## Getting a Google Apps API key (Required!)

* Create an application [here](https://console.developers.google.com)
* On the API Manager section, go to "Credentials" and create a new API key
* Enable your application to communicate the YouTube Api [here](https://console.developers.google.com/apis/api/youtube)
* Make sure the following URL works for you in your browser (Change the key at the end!):
https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCu7_D0o48KbfhpEohoP7YSQ&key=PutYourNewlyGeneratedKeyHere

