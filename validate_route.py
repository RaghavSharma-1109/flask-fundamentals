import json
from flask import Flask , jsonify, request 

app = Flask(__name__)
items = []
@app.route('/items' , methods=['POST'])
def post_item():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    id = len(items) +1
    add_item = {'data': data, 'id': id}
    items.append(add_item)

    return jsonify(add_item), 201

@app.route('/items')
def get_item():
    if not items:
        return jsonify({"'error": 'No items'})
    return jsonify(items)

@app.route('/items/<int:id>')
def get_item_by_id(id):
    for item in items:
        if item['id'] == id:
            return jsonify(item), 200
    return jsonify({"error":'item not found'}), 404

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item_by_id(id):
    for item in items:
        if item['id'] == id:
            items.remove(item)
            return jsonify(item), 200
    return jsonify({"error":'item not found'}), 404

if __name__=='__main__':
    app.run(debug=True)