from flask import Flask, render_template, url_for, redirect
from views import dht_both, uptime
import json

with open("app.json") as f:
  config = json.load(f)

app = Flask(__name__)
blueprints = []
for x in config['modules']:
    module = x['view'] + "." + x['view']
    command = "(\"" + x['name']+"\",x)"
    bp = eval(module+command)
    blueprints.append(bp)
    app.register_blueprint(bp.view,url_prefix="/"+x['name'])
    
bp = uptime.uptime("test",{"title":"asdas"})
bp2 = uptime.uptime("test2",{"title":"asdasasdasdasdasd"})
app.register_blueprint(bp.view,url_prefix="/test")
app.register_blueprint(bp2.view,url_prefix="/test2")

@app.route('/')
def index2():
  return render_template('index.html',title = config['app']['title'])

@app.route('/index')
def index():
  return redirect(url_for('/'))
  

if __name__ == "__main__":
  app.run(debug=True)
