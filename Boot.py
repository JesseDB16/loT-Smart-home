#import webrepl
#webrepl.start()

import time
import network
import config as c
from umqtt.robust import MQTTClient

#%% connect to WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# wait for WiFi connection and print configuration when it has connected
def checkwifi():
    if not sta_if.isconnected():
        sta_if.connect(c.WLAN_SSID, c.WLAN_PASS)
        print("Connecting", end="")
        while not sta_if.isconnected():
            time.sleep_ms(500)
            print(".", end="")
        print(sta_if.ifconfig())

checkwifi()

#%% start MQTT client
enable = True

# callback function for incoming messages
def on_message_received(topic, msg):
    global enable
    print(topic, msg)
    if msg == b'toggle':
        enable = not enable

# create MQTT client object
client = MQTTClient(c.CLIENTID, c.BROKER, port=c.PORT, user=c.HA_USER, password=c.HA_PASS)
client.DEBUG=False
client.reconnect()                                      # ensures the MQTT client is connected
client.set_callback(on_message_received)                # set the callback function for incoming messages

# create subscriptions and publish connection message
client.subscribe('LED' + '/command')
client.publish('ESP32' + '/status', 'MQTT connected')
