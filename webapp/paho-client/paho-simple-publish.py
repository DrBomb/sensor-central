import paho.mqtt.publish as mqtt
import time
count = 0
while True:
    mqtt.single("/simple/counter",count)
    print count
    count = count + 1
    time.sleep(1)


