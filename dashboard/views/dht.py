from flask import Blueprint, render_template, abort, Response
from jinja2 import TemplateNotFound
from datetime import datetime
from json import dumps
from new import classobj
from ..database.database import db


class dht:
    def __init__(self,params):
        self.view = Blueprint(params['name'],__name__,template_folder='templates')
        self.title = params['title']
        self.mqtt_temperature = params['mqtt_feeds'][0]
        self.mqtt_humidity = params['mqtt_feeds'][1]
        self.mqtt_feeds = params['mqtt_feeds']
        self.name = params['name']
        self.table = classobj(self.name,(db.Model,),{
            "__tablename__": self.name,
            "id" : db.Column(db.Integer,primary_key=True),
            "data_type" : db.Column(db.Enum("hum","temp")),
            "value":db.Column(db.Float),
            "timestamp" : db.Column(db.DateTime)
            })
        self.set_view_params(params)
        @self.view.route('/')
        def index(): 
            return render_template('dht.html',params=self)
        @self.view.route('/dht.js')
        def dht_js():
            return Response(render_template('js/dht.js',params=self),mimetype="text/javascript")
        @self.view.route('/temperature/')
        @self.view.route('/temperature/<int:count>')
        def temperature(count=10):
            query = self.table.query.filter(self.table.data_type == 'temp').order_by(self.table.timestamp.desc()).limit(count)
            results = []
            for x in query:
                results.append((x.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),x.value,))
            return dumps(results)
        @self.view.route('/humidity/')
        @self.view.route('/humidity/<int:count>')
        def humidity(count=10):
            results = []
            for x in self.table.query.filter(self.table.data_type == "hum").limit(count):
                results.append((x.value,x.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),))
            return dumps(results)
        @self.view.record
        def record_params(setup_state):
            self.app = setup_state.app
    def set_view_params(self,params):
        self.plot_points = (params['plot_points'] if 'plot_points' in params.keys() 
                else 20)
        self.update_delay = (params['update_delay'] if 'update_delay' in params.keys()
                else 10000)
    def record(self,msg):
        if msg.topic == self.mqtt_temperature:
            entry = self.table(value=float(msg.payload),timestamp=datetime.now(),\
                    data_type='temp')
            with self.app.app_context():
                db.session.add(entry)
                db.session.commit()
        if msg.topic == self.mqtt_humidity:
            entry = self.table(value=float(msg.payload),timestamp=datetime.now(),\
                    data_type='hum')
            with self.app.app_context():
                db.session.add(entry)
                db.session.commit()

