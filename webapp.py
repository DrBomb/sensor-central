from dashboard.views.dht import dht
from dashboard.views.simple import Simple
from dashboard.dashboard import App
views = [dht({
    "name": "DHT1",
    "title": "DHT11",
    "mqtt_feeds": [
        "/dht1/temperature",
        "/dht1/humidity"
        ]
    }),
    Simple({
        "name": "Simple",
        "title": "Simple",
        "mqtt_feeds": [
            "/simple/counter"
        ]
    })]

app = App(views,database_uri="sqlite:///log.sqlite")
app.start_mqtt()
if __name__ == "__main__":
    app.app.run(debug=True)
