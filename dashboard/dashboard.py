from flask import Flask, render_template, url_for, redirect
from threading import Thread
import mqtt
from zc import lockfile
from database.database import db

class App(object):
    def __init__(self,views,database_uri='sqlite:///:memory:',mqtt_host="localhost"):
        self.app = Flask(__name__)
        self.views = views
        self.mqtt_host = mqtt_host
        self.app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        self.app.config['SQLALCHEMY_ECHO'] = False
        db.init_app(self.app)
        self.register_views()
        @self.app.route('/')
        def index():
            return render_template('index.html', title="Sensor Central",views=self.views)
        @self.app.route('/index')
        def index2():
            return redirect(url_for('/'))
    def register_views(self):
        for x in self.views:
            self.app.register_blueprint(x.view, url_prefix='/' + x.name)
        with self.app.app_context():
            db.create_all()
    def start_mqtt(self):
        try:
            self.lock = lockfile.LockFile('lock')
            mqtt.views = self.views
            mqtt.mqtt.connect(self.mqtt_host)
            worker = Thread(target=mqtt.mqtt.loop_forever)
            worker.daemon = True
            worker.start()
        except lockfile.LockError:
            print("Can't lock file")
        
