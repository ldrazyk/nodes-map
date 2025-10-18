from flask import jsonify, request, redirect, url_for
from . import api
from app import application
from pprint import pprint

@api.route('/')
def api_home():
    return "This is API"

@api.route('/map')
def get_map():

    id = request.args["id"]
    map_data = application.get_map(id)
    if "image" in map_data["nodes"][0]:
        for node in map_data["nodes"]:
            if "image" in node:
                node["image"] = url_for('static', filename=f"images/{node["image"]}")
    return jsonify(map_data)

@api.post('/map/example')
def get_map_example():

    data = request.get_json()
    map_data = application.get_map_example(data.get('id'))
    return jsonify(map_data)

@api.post('/map/create')
def create_map():

    def get_form_dict():

        form = request.form.to_dict(flat=False)

        for key, value in form.items():

            if len(value) == 1:
                form[key] = value[0]
        
        return form

    def create_spec(form:dict):

        def filter_form(form:dict, projection:dict):

            def convert(value:str, target_type:type):

                if target_type in [int, float, bool]:
                    return target_type(value)
                else:
                    return value

            return { projection[key][0]: convert(value, projection[key][1]) for key, value in form.items() if key in projection }

        def create_api_spec(form:dict):

            projection = {
                "spec-src": ["url", str],
                "spec-id": ["id", str]
            }
            
            return filter_form(form, projection)
        
        def create_preprocess_spec(form:dict):

            projection = {
                "standardize-features": ["standardize_features", bool],
                "normalize": ["normalize", bool],
                "reduce": ["reduce", bool],
                "normalize-reduce-input": ["normalize_reduce_input", bool],
                "reduction-size": ["reduction_size", int],
                "normalize-reduce-output": ["normalize_reduce_output", bool],
                "combine": ["combine", bool],
                "normalize-combine-input": ["normalize_combine_input", bool],
                "input-reduction-size": ["input_reduction_size", int],
                "output-reduction-size": ["output_reduction_size", int],
                "normalize-combine-output": ["normalize_combine_output", bool],
            }

            return filter_form(form, projection)
        
        def create_mapping_spec(form:dict):

            projection = {
                "cluster": ["cluster", bool],
                "min-cluster": ["min_cluster", int],
                "max-cluster": ["max_cluster", int],
                "metric": ["metric", str],
                "n-neighbors": ["n_neighbors", int],
                "random-state": ["random_state", int],
                "min-distance": ["min_distance", float],
                "spread": ["spread", float]
            }

            return filter_form(form, projection)
        
        return {
            "map_name": form["map-name"],
            "api": create_api_spec(form),
            "preprocess": create_preprocess_spec(form),
            "mapping": create_mapping_spec(form)
        }


    pprint(request.form)
    # for key, value in form.items():
    #     print(f"{key}: {value}")

    form = get_form_dict()
    pprint(form)
    spec = create_spec(form)
    pprint(spec)
    
    id = application.create_map(spec)

    return redirect(url_for("main.show_map", id=id))

@api.route('/nodes/spec')
def get_nodes_spec():

    id = request.args.get("id")
    nodes_spec = application.get_nodes_spec(id)
    return jsonify(nodes_spec)

@api.post('/embeddings/combine')
def combine_embeddings():

    data = request.get_json()
    result = application.combine_embeddings(embeddings_models=data.get('embeddings'), 
                                        input_reduction_size=data.get('input_reduction_size'), 
                                        final_size=data.get('final_size'), 
                                        normalize_input=data.get('normalize_input', True),
                                        normalize_output=data.get('normalize_output', True),
                                        to_lists=True)

    return jsonify(result)

@api.post('embeddings/normalize')
def normalize_embeddings():

    data = request.get_json()
    result = application.normalize_embeddings(embeddings=data.get('embeddings'), to_lists=True)

    return jsonify(result)

@api.post('/embeddings/reduce')
def reduce_embeddings():

    data = request.get_json()
    result = application.reduce_embeddings(embeddings=data.get('embeddings'), 
                                        reduction_size=data.get('reduction_size'), 
                                        normalize_input=data.get('normalize_input', True),
                                        normalize_output=data.get('normalize_output', True),
                                        to_lists=True)

    return jsonify(result)
