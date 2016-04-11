from flask import Flask, render_template, url_for, redirect
from threading import Thread
import mqtt
from database.database import db
from dht import dht
from simple import Simple

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    return app

app = create_app()
views = [dht({
    "name":"DHT1",
    "title":"DHT11",
    "mqtt_feeds":[
        "/dht1/temperature",
        "/dht1/humidity"
        ],
    "app":app
    }),
    Simple({
    "name":"Simple",
    "title":"Simple",
    "mqtt_feeds":[
        "/simple/counter"
        ],
    "app":app
    })]
for x in views:
    app.register_blueprint(x.view, url_prefix='/'+x.name)
with app.app_context():
    db.create_all()
mqtt.views = views
mqtt.mqtt.connect("localhost")
#if getattr(app, 'background_thread', None) is None:
#    worker = Thread(target=mqtt.mqtt.loop_forever)
#    worker.daemon = True
#    worker.start()
#    app.background_thread = worker
@app.route('/')
def index2():
    return render_template('index.html',title = config['app']['title'])
@app.route('/index')
def index():
    return redirect(url_for('/'))
if __name__ == "__main__":
    app.run(debug=False)
