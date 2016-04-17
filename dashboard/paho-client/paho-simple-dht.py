import paho.mqtt.publish as mqtt
import time
count = 0.5
while True:
    mqtt.single("/dht1/temperature",count)
    print count
    count = count + 1
    time.sleep(1)


