from flask import Blueprint, jsonify,request
from extensions import db
from model import Item

items_bp = Blueprint('items',__name__)

@items_bp.route('/items')
def get_item():
    data=Item.query.all()
    items=[]
    for item in data:
        new_item = {'id':item.id, 'name':item.name, 'price': item.price}
        items.append(new_item)
    
    return jsonify(items),200

@items_bp.route('/items/<int:id>')
def get_item_by_id(id):
    data = Item.query.get(id)
    if not data:
        return jsonify({'error':f'item by id:{id} not found'}), 400
    return jsonify({'id':data.id,'name':data.name,'price':data.price}), 200

@items_bp.route('/items',methods=['POST'])
def add_item():
    data = request.json
    if not data or not isinstance(data,dict):
        return jsonify({"error":'Invalid request data'}), 400
    if 'name' not in data or 'price' not in data:
        return jsonify({'error':'Missing a Key in data'}), 400
    new_item = Item(name=data['name'], price=data['price'])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'id':new_item.id, 'name':new_item.name, 'price': new_item.price}), 201

# @items_bp.route('/items/<int:id>', mwthods=['POST'])
# def add_item_by_id(id):
#     data = request.json
#     if not data or not isinstance(data,dict):
#         return jsonify({"error":'Invalid request data'}), 400
#     if 'name' not in data or 'price' not in data:
#         return jsonify({'error':'Missing a Key in data'}), 400
#     if Item.query.get(id):
#         return jsonify({'error': f'Item by id:{id} already exists'}), 400
    
@items_bp.route('/items/<int:id>',methods=['DELETE'])
def del_item_by_id(id):
    entry=Item.query.get(id)
    if not entry:
        return jsonify({'error':f"item by id:{id} does not exists"}), 400
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message':f'item by id: {id} successfully deleted'}), 200

