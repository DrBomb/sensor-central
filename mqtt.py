from paho.mqtt.client import Client

views = []

def on_connect(client,userdata,rc):
    print ("Connected Code: " + str(rc))
    if views == []:
        raise NotImplementedError
    for x in views:
        for y in x.mqtt_feeds:
            client.subscribe(y)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    for x in views:
        for y in x.mqtt_feeds:
            if(y==msg.topic):
                x.record(msg)

mqtt = Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message
