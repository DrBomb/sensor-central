from flask import Blueprint, render_template
from datetime import datetime
from json import dumps
from new import classobj
from database.database import db

class Simple:
    def __init__(self,params):
        self.view = Blueprint(params['name'],__name__,template_folder='templates')
        self.app = params['app']
        self.title = params['title']
        self.mqtt_feeds = params['mqtt_feeds']
        self.name = params['name']
        self.table = classobj(self.name,(db.Model,),{
            "__tablename__":self.name,
            "id":db.Column(db.Integer,primary_key=True),
            "value":db.Column(db.Integer),
            "timestamp":db.Column(db.DateTime)
            })
        @self.view.route('/')
        def index():
            response = "["
            for x in self.table.query.all():
                response += "{"
                response += "\"value\":\""
                response += str(x.value)
                response += "\",\"timestamp\":\""
                response += str(x.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                response += "\"},"
            response = response[:-1]
            response += "]"
            return response
        @self.view.record
        def record_params(setup_state):
            self.app = setup_state.app
    def record(self,msg):
        entry = self.table(value=msg.payload,timestamp=datetime.now())
        with self.app.app_context():
            db.session.add(entry)
            db.session.commit()
