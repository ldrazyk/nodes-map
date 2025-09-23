from flask import render_template
from . import main
from app import app_model

@main.route('/')
def home():
    print(app_model.to_string())
    return render_template('home.html')