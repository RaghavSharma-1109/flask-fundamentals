import json
from flask import Flask, jsonify,request
app = Flask(__name__)
items =[]
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    if not data or 'name' not in data  :
        return jsonify({'error':"name is required"}), 400
    new_id = len(items) + 1
    add = {'data': data, 'id': new_id}
    items.append(add)
    return jsonify(add), 201

@app.route('/items')
def get_item():
    if not items:
        return {}
    return items

@app.route('/items/<int:id>')
def get_item_id(id):
    found=0
    for item in items:
        if item['id'] == id:
            found =1
            return item
    if found==0:
        return jsonify({"error":'item not found'}),404

@app.route("/items/<int:id>", methods=['DELETE'])
def del_item(id):
    found=0
    for item in items:
        if item['id'] == id:
            found =1
            items.remove(item)
            return jsonify({"message":"item deleted"}),200
    if found==0:
        return jsonify({"error":'item not found'}),404

if __name__=='__main__':
    app.run(debug=True)