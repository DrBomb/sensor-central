from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)

with open("app.json") as file:
  config = json.loads(file)

@app.route('/')
def index2():
  return redirect(url_for('index'))

@app.route('/index')
def index():
  return render_template('index.html',title = "Pagina Principal", views = data)

if __name__ == "__main__":
  app.run(debug=True)
