from micropython_youtube_api import YoutubeApi
import network, json, time

with open('config.json') as f:
    config = json.load(f)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect( config['ssid'], config['ssid_password'])

while not wlan.isconnected:
    pass

with YoutubeApi( wlan, config ) as data:

    update_interval = 10

    while True:

        print ("Subs " + str( data.subs ) )
        print ("Views " + str( data.views ) )

        print ("Sleeping for {} secs".format(update_interval) )
        time.sleep( update_interval )
