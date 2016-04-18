# coding: utf-8
from flask import Blueprint, render_template, abort, Response
from jinja2 import TemplateNotFound
from datetime import datetime
from json import dumps
from new import classobj
from ..database.database import db
import sys

class SimpleGraph:
    def __init__(self,params):
        self.view = Blueprint(params['name'],__name__,template_folder='templates')
        self.mqtt_feeds = params['mqtt_feeds']
        self.name = params['name']
        self.table = classobj(self.name,(db.Model,),{
            "__tablename__": self.name,
            "id" : db.Column(db.Integer,primary_key=True),
            "value":db.Column(db.Float),
            "timestamp" : db.Column(db.DateTime)
            })
        self.set_view_params(params)
        @self.view.route('/')
        def index(): 
            return render_template('SimpleGraph.html',params=self)
        @self.view.route('/SimpleGraph.js')
        def dht_js():
            return Response(render_template('js/SimpleGraph.js',params=self),mimetype="text/javascript")
        @self.view.route('/reading/')
        @self.view.route('/reading/<int:count>')
        def reading_query(count=10):
            results = []
            for x in self.table.query.order_by(self.table.timestamp.desc()).limit(count):
                results.append((x.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),x.value,))
            return dumps(results)
        @self.view.record
        def record_params(setup_state):
            self.app = setup_state.app
    def set_view_params(self,params):
        params = params['view_params']
        self.plot_points = (params['plot_points'] if 'plot_points' in params.keys() 
                else 20)
        self.update_delay = (params['update_delay'] if 'update_delay' in params.keys()
                else 10000)
        self.plot_colour = (params['plot_colour'] if 'plot_colour' in params.keys()
                else "#a31515")
        self.scale_label = (params['scale_label'] if 'scale_label' in params.keys()
                else "<%=value%>")
        self.title = (params['title'] if 'title' in params.keys()
                else None)
    def record(self,msg):
        if msg.topic == self.mqtt_feeds[0]:
            entry = self.table(value=float(msg.payload),timestamp=datetime.now())
            with self.app.app_context():
                db.session.add(entry)
                db.session.commit()
