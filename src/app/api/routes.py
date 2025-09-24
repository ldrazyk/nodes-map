from flask import jsonify, request, Response
from . import api
from app import embeddings_processor

@api.route('/')
def api_home():
    return "This is API"

@api.post('/embeddings/combine')
def combine_embeddings():

    data = request.get_json()
    result = embeddings_processor.combine_embeddings(embeddings_models=data.get('embeddings'), 
                                        input_reduction_size=data.get('input_reduction_size'), 
                                        final_size=data.get('final_size'), 
                                        normalize_input=data.get('normalize_input', True),
                                        normalize_output=data.get('normalize_output', True),
                                        to_lists=True)

    return jsonify(result)

@api.post('embeddings/normalize')
def normalize_embeddings():

    data = request.get_json()
    result = embeddings_processor.normalize_embeddings(embeddings=data.get('embeddings'), to_lists=True)

    return jsonify(result)

@api.post('/embeddings/reduce')
def reduce_embeddings():

    data = request.get_json()
    result = embeddings_processor.reduce_embeddings(embeddings=data.get('embeddings'), 
                                        reduction_size=data.get('reduction_size'), 
                                        normalize_input=data.get('normalize_input', True),
                                        normalize_output=data.get('normalize_output', True),
                                        to_lists=True)

    return jsonify(result)
