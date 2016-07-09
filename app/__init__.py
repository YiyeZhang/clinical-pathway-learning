from flask import Flask
import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__,template_folder=tmpl_dir)
app.config.from_object('config')

from app import views
