import json
from os import name
from flask import Flask , jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///items.db'
db = SQLAlchemy(app)
migrate=Migrate(app,db)
class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Float,nullable=False)

@app.route('/items' , methods=['POST'])
def post_item():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    new_item=Item(name=data['name'], price = data['price'])
    #comminting: sutomatically adds id
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'id':new_item.id, 'name':new_item.name, 'price': new_item.price}), 201

@app.route('/items')
def get_item():
    data = Item.query.all()
    items = []
    for entry in data:
        new_items = {'id':entry.id,'name':entry.name, 'price':entry.price}
        items.append(new_items)
    return jsonify(items), 200
            
@app.route('/items/<int:id>')
def get_item_by_id(id):
    entry = Item.query.get(id)
    if not entry:
        return jsonify({"error": f"No item found by id: {id}"}), 404
    return jsonify({'id': entry.id, 'name': entry.name, 'price': entry.price}), 200

@app.route('/items/<int:id>',methods=['DELETE'])
def del_item_by_id(id):
    entry = Item.query.get(id)
    if not entry:
        return jsonify({"error": f"No item found by id: {id}"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": f"Item by id: {id} DELETED successfully"})


if __name__=='__main__':
    app.run(debug=True)