from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

class dht_both:
  def __init__(self,name,params):
    self.view = Blueprint(name,__name__,template_folder="templates")
    self.params = params
    @self.view.route('/')
    def index(): 
      return render_template('dht_both.html',params=self.params)
