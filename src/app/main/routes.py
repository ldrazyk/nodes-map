from flask import render_template, request, jsonify
from . import main
from app import application

@main.route('/')
def show_form():

    map_ids = application.get_map_ids()
    map_ids.sort()

    return render_template('form.html', map_ids=map_ids)

@main.route('/map')
def show_map():

    map_id = request.args.get("id")
    
    return render_template('map.html', map_id=map_id)

@main.route('/map/test')
def test_map():

    id = request.args.get("mapId")

    return f"This is '{id}' map."