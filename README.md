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

## Using the API

Check the grab_stats.py example script for a full implementation of using the library.

Take note that the creation of the YoutubeAPI() instance is done using the **with** statement to create a context around the definition, so cleanup of the WiFi connection can happen when the data variable (class instance) is out of scope. 

.. code-block:: python
    from micropython_youtube_api import YoutubeAPI
    import network, json, time

    # Read config
    with open('config.json') as f:
        config = json.load(f)

    # Create WiFi connection and turn it on
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Connect to WiFi router
    print ("Contacting to WiFi: {}".format( config['ssid'] ) )
    wlan.connect( config['ssid'], config['ssid_password'])

    # Wait until wifi is connected
    while not wlan.isconnected:
        pass

    # Create an instance of the YoutubeApi
    with YoutubeAPI( wlan, config ) as data:

        # Read the data every X seconds
        update_interval = 10

        while True:
            print ("Subs {}".format( data.subs ) )
            print ("Views {}".format( data.views ) )
            print ("Videos {}".format( data.videos ) )
            print ("Comments {}".format( data.comments ) )

            # Sleep for a bit... until the next call
            print ("Sleeping for {} secs".format( update_interval ) )
            time.sleep( update_interval )
..

## Getting a Google Apps API key (Required!)

* Create an application [here](https://console.developers.google.com)
* On the API Manager section, go to "Credentials" and create a new API key
* Enable your application to communicate the YouTube Api [here](https://console.developers.google.com/apis/api/youtube)
* Make sure the following URL works for you in your browser (Change the key at the end!):
https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCu7_D0o48KbfhpEohoP7YSQ&key=PutYourNewlyGeneratedKeyHere

