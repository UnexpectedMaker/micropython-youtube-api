from micropython_youtube_api import YoutubeApi
import time

data = YoutubeApi()

while True:
    if not data.running:
        data.grabStats()

    print ("Subs " + str( data.subs ) )
    print ("Views " + str( data.views ) )

    print ("Sleeping for " + str( data.update_interval ) + "secs")
    time.sleep( data.update_interval )