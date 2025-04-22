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
    
    nodes_file = request.form.get('nodes_file')
    
    return jsonify({'nodes_file': nodes_file})

if __name__ == '__main__':
    app.run(debug=True, port=5007)