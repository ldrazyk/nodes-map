from flask import Flask, render_template, jsonify, request
from model.Model import Model

app = Flask(__name__)

model = Model()


@app.route("/")
def index():
    files_list = model.get_node_files_list()
    return render_template('index.html', files=files_list)

@app.post("/map")
def show_map():
    
    map_name = request.form.get('map_name')
    
    nodes_file = request.form.get('nodes_file')
    nodes = model.get_nodes_data(nodes_file)
    
    if nodes:
        
        extremes = model.get_extremes(nodes)
        
        def print_data():
            data = {'map_name': map_name, 'nodes': nodes, 'extremes': extremes}
            print(data)
            
        print_data()
        
        return render_template('map_pixi.html', map_name=map_name, nodes=nodes, extremes=extremes)
    
    else:
        return "Nodes not found!"

if __name__ == '__main__':
    app.run(debug=True, port=5007)