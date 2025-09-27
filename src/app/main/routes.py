from flask import render_template
from . import main

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/map')
def show_map():
    return render_template('map.html')