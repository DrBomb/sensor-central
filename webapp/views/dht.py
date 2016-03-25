from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime
from json import dumps
from .database import db
class dht:
    def __init__(self,params):
        self.view = Blueprint(params['name'],__name__,template_folder="templates")
        self.title = params['title']
        self.mqtt_feeds = params['mqtt_feeds']
        self.name = params['name']
        self.table = class (db.Model):
            id = db.Column(db.Integer,primary_key=True)
            data_type = db.Column(db.Enum(("hum","temp")))
            timestamp = db.Column(db.DateTime)
        @self.view.route('/')
        def index(): 
            return render_template('dht_both.html',params=self.params)
        @self.view.route('/temperature/<int:count>')
        def temperature(count):
            session = self.Session()
            results = session.query(self.table).all()
            return dumps(results)
