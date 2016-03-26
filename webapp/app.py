from flask import Flask, render_template, url_for, redirect
from database.database import db
from dht import dht

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    return app

if __name__ == "__main__":
  app = create_app()
  dht1 = dht({
      "name":"DHT1",
      "title":"DHT11",
      "mqtt_feeds":[
          "/dht1/temperature",
          "/dht1/humidity"
          ]
      })
  dht2 = dht({
      "name":"DHT2",
      "title":"DHT2",
      "mqtt_feeds":[
          "/dht2/temperature",
          "/dht2/humidity"
          ]
      })
  app.register_blueprint(dht1.view, url_prefix='/'+dht1.name)
  app.register_blueprint(dht2.view, url_prefix='/'+dht2.name)
  with app.app_context():
      db.create_all()
  @app.route('/')
  def index2():
      return render_template('index.html',title = config['app']['title'])
  @app.route('/index')
  def index():
      return redirect(url_for('/'))
  app.run(debug=True)
