# coding: utf-8
from dashboard.views.SimpleGraph import SimpleGraph
from dashboard.views.simple import Simple
from dashboard.dashboard import App
views = [SimpleGraph({
    "name": "temperature1",
    "mqtt_feeds": [
        "dht11/temp"
        ],
    "view_params": {
        "title":"Temperatura",
        "scale_label":"<%=value%>ºC"
        }
    }),
    SimpleGraph({
    "name": "humidity1",
    "mqtt_feeds": [
            "dht11/hum"
        ],
    "view_params": {
        "title":"Humedad",
        "plot_colour":"#4185D8",
        "scale_label":"<%=value%>%"
        }
    })]

app = App(views,database_uri="sqlite:///log.sqlite",mqtt_host="iot.eclipse.org")
app.start_mqtt()
if __name__ == "__main__":
    app.app.run(debug=True)
