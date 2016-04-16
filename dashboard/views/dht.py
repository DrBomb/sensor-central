from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime
from json import dumps
from new import classobj
from ..database.database import db


class dht:
    def __init__(self,params):
        self.view = Blueprint(params['name'],__name__,template_folder='templates')
        self.title = params['title']
        self.mqtt_feeds = params['mqtt_feeds']
        self.name = params['name']
        self.table = classobj(self.name,(db.Model,),{
            "__tablename__": self.name,
            "id" : db.Column(db.Integer,primary_key=True),
            "data_type" : db.Column(db.Enum("hum","temp")),
            "timestamp" : db.Column(db.DateTime)
            })
        @self.view.route('/')
        def index(): 
            return render_template('dht.html',params={"title":self.name})
        @self.view.route('/temperature/<int:count>')
        def temperature(count):
            session = self.Session()
            results = session.query(self.table).all()
            return dumps(results)
