from micropython_youtube_api import YoutubeAPI
import network, json, time

# Read config
with open('config.json') as f:
    config = json.load(f)

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

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
