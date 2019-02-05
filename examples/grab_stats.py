from micropython_youtube_api import YoutubeApi
import time

try:
    data = YoutubeApi()
    update_interval = 10

    while True:

        print ("Subs " + str( data.subs ) )
        print ("Views " + str( data.views ) )

        print ("Sleeping for " + str( update_interval) + "secs")
        time.sleep( update_interval )
except KeyboardInterrupt:
        data.shutdown()
        raise