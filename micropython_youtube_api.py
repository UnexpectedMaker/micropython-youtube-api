# The MIT License (MIT)
#
# Copyright (c) 2019 Seon "Unexpected maker" Rozenblum
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

See examples folder for how to use

* Author(s): Seon Rozenblum
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/unexpectedmaker/micropython-youtube-api"

import urequests as ureq
import network, json, time

class YoutubeAPI:

    coonnections = 0

    update_stats_time = time.time() - 10

    cached_subs = 0
    cached_views = 0
    cached_comments = 0
    cached_videos = 0

    def __init__(self, conn, conf ):

        if YoutubeAPI.coonnections == 0:
            # set connections to 1 so we can have any more instances
            YoutubeAPI.coonnections == 1

            YoutubeAPI.config = conf
            YoutubeAPI.conn = conn

        else:
            print("You don't need more than one instance...")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.shutdown()

    def update_stats(self):
        if YoutubeAPI.update_stats_time < time.time():
            YoutubeAPI.grab_stats()
            YoutubeAPI.update_stats_time = time.time() + YoutubeAPI.config['query_interval_sec']

    @classmethod
    def grab_stats(cls):

        if YoutubeAPI.conn.isconnected:
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
        return YoutubeAPI.cached_subs

    @property
    def views(self):
        self.update_stats()
        return YoutubeAPI.cached_views

    @property
    def videos(self):
        self.update_stats()
        return YoutubeAPI.cached_videos

    @property
    def comments(self):
        self.update_stats()
        return YoutubeAPI.cached_comments

    # Shutdown wifi if exiting class instance
    def shutdown(self):
        if YoutubeAPI.conn.isconnected():
            YoutubeAPI.conn.active(False)

