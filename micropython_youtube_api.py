# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George (original Neopixel object)
# Copyright (c) 2017 Ladyada
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2019 Matt Trentini (porting back to MicroPython)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`micropython_youtube_api` - YouTube API 
====================================================

* Author(s): Seon Rozenblum
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/unexpectedmaker/micropython-youtube-api"

import network
import urequests as ureq
import json
import time

class YoutubeApi:

    config = {}
    coonnections = 0
    running = False
    update_interval = 0
    has_internet = False

    subs = 0
    views = 0

    def __init__(self):

        if YoutubeApi.coonnections == 0:
            # Read config
            with open('config.json') as f:
                YoutubeApi.config = json.load(f)

            #store update interval 
            YoutubeApi.update_interval = YoutubeApi.config['query_interval_sec']

            # set connections to 1 so we can have any more instances
            YoutubeApi.coonnections == 1
            YoutubeApi.has_internet = False
        else:
            print("You don't need more than one instance...")

    def grabStats(self):

        if not YoutubeApi.running:

            if not YoutubeApi.has_internet:

                YoutubeApi.wlan = network.WLAN(network.STA_IF)
                YoutubeApi.wlan.active(True)

                if not YoutubeApi.wlan.isconnected():
                
                    print('connecting to network...')

                    YoutubeApi.wlan.connect(config['ssid'], config['ssid_password'])
                    while not YoutubeApi.wlan.isconnected():
                        pass
                    print("Connected!")
                    YoutubeApi.has_internet = True

            YoutubeApi.running = True

            command = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+ YoutubeApi.config['channelid'] + "&key=" + YoutubeApi.config['appid']
            #print ( command )
            print ("Contacting GoogleAPI...")

            req = ureq.get( command )
            
            if req.status_code == 200:
                YoutubeApi.stats = [{'subs': stat['statistics']['subscriberCount'], 'views': stat['statistics']['viewCount']} for stat in req.json()['items']]
                
                # for stat in YoutubeApi.stats
                YoutubeApi.subs = YoutubeApi.stats[0]['subs']
                YoutubeApi.views = YoutubeApi.stats[0]['views']

            else:
                print( "ERROR: status_code: " + str(req.status_code) )

            # print ("Sleeping for " + str( YoutubeApi.config['query_interval_sec'] ) + "secs")
            # # time.sleep( YoutubeApi.config['query_interval_sec'] )

            YoutubeApi.running = False

    def __exit__(self):
        YoutubeApi.running = False
        wlan.active(False)