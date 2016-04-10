from paho.mqtt.publish import single
import time
count = 0
while True:
    single("/simple/counter", count)
    print count
    count += 1
    time.sleep(1)


