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
    nodes_data = model.get_nodes_data(nodes_file)
    
    data = {'map_name': map_name, 'nodes': nodes_data}
    print(data)
    
    return render_template('map.html', map_name=map_name, nodes=nodes_data)

if __name__ == '__main__':
    app.run(debug=True, port=5007)