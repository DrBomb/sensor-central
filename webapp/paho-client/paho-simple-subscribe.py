from paho.mqtt.client import Client

def on_connect(client, userdata, rc):
    client.subscribe("/simple/counter")
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
client = Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect("localhost")
client.loop_forever()
