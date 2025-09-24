from flask import jsonify, request, Response
from . import api
from app import utils

@api.route('/')
def api_home():
    return "This is API"

@api.post('/embeddings/combine')
def combine_embeddings():

    data = request.get_json()
    combined = utils.combine_embeddings_models(embeddings_models=data.get('embeddings'), 
                                               input_reduction_size=data.get('reduction_size'), 
                                               final_size=data.get('final_size'), 
                                               normalize_input=data.get('normalize_input', True),
                                               normalize_output=data.get('normalize_output', True),
                                               to_lists=True)

    return jsonify(combined)