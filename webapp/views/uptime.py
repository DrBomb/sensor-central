from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

class uptime:
  def __init__(self,name,params):
    self.view = Blueprint(name,__name__,template_folder='templates')
    self.params = params
    @self.view.route("/")
    def index():
      return render_template('uptime.html',title=self.params['title'])