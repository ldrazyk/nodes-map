from flask import Flask, render_template, jsonify, request
from model.Model import Model

app = Flask(__name__)

model = Model()

@app.route("/")
def index():
    return render_template('index.html')

@app.post("/map")
def show_map():
    data = request.get_json()
    return request

if __name__ == '__main__':
    app.run(debug=True, port=5007)