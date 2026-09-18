import json
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

@items_bp.route('/items/<int:id>/',methods = ['PUT'])
def put_by_id(id):
    required = {'price', 'name'}
    data = request.json
    item=Item.query.get(id)
    if not item:
        return jsonify({'error':f'Item with id: {id} not found'}), 404
    keys = list(data.keys())
    if set(keys) != required:
        return jsonify({'error':'field missing or invalid field'}), 400
    for key in keys: 
        if key == 'price' and not isinstance(data[key],(int,float)):
            return jsonify({'error': 'Invalid data type for field: price'}), 400
        if key == 'price' and data[key]<=0:
            return jsonify({'error': 'Invalid value for field: price'}), 400
        if key == 'name' and not isinstance(data[key],str):
            return jsonify({'error': 'Invalid value for field: name'}), 400
        setattr(item,key,data[key])        

    db.session.commit()

    return jsonify({'message':'field updated'}), 200
    
@items_bp.route('/items/<int:id>',methods=['PATCH'])
def patch_by_id(id):
    required = {'price', 'name'}
    data = request.json
    item=Item.query.get(id)
    if not item:
        return jsonify({'error':f'Item with id: {id} not found'}), 404
    keys = list(data.keys())
    if not keys:
        return jsonify({'error':'Empty fields'}), 400
    if not set(keys).issubset(required):
        return jsonify({'error': 'Invalid or missing field'}), 400
    if 'id' in keys:
        return jsonify({'error': 'id can not be patched'}), 400
    for key in keys:
        if key == 'price' and not isinstance(data[key],(int,float)):
            return jsonify({'error': 'Invalid data type for field: price'}), 400
        if key == 'price' and data[key]<=0:
            return jsonify({'error': 'Invalid value for field: price'}), 400
        if key == 'name' and not isinstance(data[key],str):
            return jsonify({'error': 'Invalid value for field: name'}), 400
        

        setattr(item,key,data[key])
    
    db.session.commit()

    return jsonify({'message':'patched successfully'}), 200