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

    update_stats_time = time.time() - 10

    cached_subs = 0
    cached_views = 0
    cached_comments = 0
    cached_videos = 0

    def __init__(self, conn, conf ):

        if YoutubeApi.coonnections == 0:
            # set connections to 1 so we can have any more instances
            YoutubeApi.coonnections == 1
            
            YoutubeApi.config = conf
            YoutubeApi.conn = conn

        else:
            print("You don't need more than one instance...")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.shutdown()

    def update_stats(self):
        if YoutubeApi.update_stats_time < time.time():
            YoutubeApi.grab_stats()
            YoutubeApi.update_stats_time = time.time() + YoutubeApi.config['query_interval_sec']

    @classmethod
    def grab_stats(cls):

        if YoutubeApi.conn.isconnected:
            command = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+ cls.config['channelid'] + "&key=" + cls.config['appid']
            #print ( command )
            print ("Contacting GoogleAPI...")

            req = ureq.get( command )
            
            if req.status_code == 200:
                cls.stats = [{
                    'subs': stat['statistics']['subscriberCount'], 
                    'views': stat['statistics']['viewCount'],
                    'videos': stat['statistics']['videoCount'],
                    'comments': stat['statistics']['commentCount']
                    } for stat in req.json()['items']]
                
                # for stat in YoutubeApi.stats
                cls.cached_subs = cls.stats[0]['subs']
                cls.cached_views = cls.stats[0]['views']
                cls.cached_videos = cls.stats[0]['videos']
                cls.comments = cls.stats[0]['comments']

            else:
                print( "ERROR: status_code: " + str(req.status_code) )
        else:
            print( "ERROR: No network connection!")

    @property
    def subs(self):
        self.update_stats()
        return YoutubeApi.cached_subs

    @property
    def views(self):
        self.update_stats()
        return YoutubeApi.cached_views

    @property
    def videos(self):
        self.update_stats()
        return YoutubeApi.cached_videos

    @property
    def comments(self):
        self.update_stats()
        return YoutubeApi.cached_comments

    def shutdown(self):
        if YoutubeApi.conn.isconnected():
            YoutubeApi.conn.active(False)
            print("Wifi Disconnected!")

