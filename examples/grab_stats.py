from micropython_youtube_api import YoutubeAPI
import network, json, time

# Read config
with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    assert False, ("config.json has not been updated with your unique keys and data")

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi router
print ("Connecting to WiFi: {}".format( config['ssid'] ) )
wlan.connect( config['ssid'], config['ssid_password'])

# Wait until wifi is connected
while not wlan.isconnected:
    pass

# Create an instance of the YoutubeApi
with YoutubeAPI( config["channelid"], config["appkeyid"], config["query_interval_sec"] ) as data:

    # Read the data every X seconds
    update_interval = 5
    update_stats_time = time.time() - 10

    while True:

        if update_stats_time < time.time():
            update_stats_time = time.time() + update_interval

            print ("Subs {}".format( data.subs ) )
            print ("Views {}".format( data.views ) )
            print ("Videos {}".format( data.videos ) )
            print ("Comments {}".format( data.comments ) )