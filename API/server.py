from flask import Flask, request, jsonify
import crud

app = Flask(__name__)

@app.before_request
def initialize():
    crud.create_table()

@app.route('/weight/<int:index>', methods=['GET'])
def get_weight(index):
    result = crud.get_weight(index)
    return jsonify(result)

@app.route('/weight', methods=['POST'])
def add_weight():
    weight = request.json.get('weight')
    residue_type = request.json.get('residue_type')
    date = request.json.get('date')
    result = crud.add_weight(weight, residue_type, date)
    return jsonify(result)

@app.route('/weight/<int:index>', methods=['PUT'])
def update_weight(index):
    weight = request.json.get('weight')
    result = crud.update_weight(index, weight)
    return jsonify(result)

@app.route('/weight/<int:index>', methods=['DELETE'])
def delete_weight(index):
    result = crud.delete_weight(index)
    return jsonify(result)

@app.route('/weight', methods=['GET'])
def get_all_weights():
    data = crud.load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
