from flask import Flask, render_template, url_for, redirect
from database import db
from views import dht

def dreate_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    return app

dht1 = dht({
    "name":"DHT1",
    "title":"DHT11",
    "mqtt_feeds":[
        "/dht1/temperature",
        "/dht1/humidity"
        ]
    })
    
app.register_blueprint(dht1.view)

@app.route('/')
def index2():
  return render_template('index.html',title = config['app']['title'])

@app.route('/index')
def index():
  return redirect(url_for('/'))
  

if __name__ == "__main__":
  app.run(debug=True)
