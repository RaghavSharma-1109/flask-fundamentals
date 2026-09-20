from flask import Blueprint,request,jsonify
from extensions import db
from model import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

user_bp = Blueprint('users',__name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data:
        return jsonify({'error':'Empty credentials'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'error':'Missing important fields'}), 400
    name = data.get('username')
    password = data.get('password')

    if not name or not password:
        return jsonify({'error': 'Empty field credentials'}), 400
    if not isinstance(name,str) or not isinstance(password,str):
        return jsonify({'error':'Invalid Field data'}), 400

    if User.query.filter_by(username=name).first():
        return jsonify({'error':'User already exists'}), 409
    hashed = generate_password_hash(password)
    new_user = User(username=name,hash_password=hashed)

    db.session.add(new_user)  
    db.session.commit()

    return jsonify({'message': 'User Registered '}), 201

@user_bp.route('/login',methods=['POST'])
def log_user():
    data = request.json
    if not data:
        return jsonify({'error':'Empty credentials'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'error':'Missing important fields'}), 400
    name = data.get('username')
    password = data.get('password')

    if not name or not password:
        return jsonify({'error': 'Empty field credentials'}), 400
    if not isinstance(name,str) or not isinstance(password,str):
        return jsonify({'error':'Invalid Field data'}), 400
    entry = User.query.filter_by(username=name).first()
    if not entry :
        return jsonify({'error':'Invalid username or password'}), 401
    if not check_password_hash(entry.hash_password, password):
        return jsonify({'error':'Invalid username or password'}), 401
    
    token = jwt.encode(
        {
            "user_id":entry.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        "Navier-stokes-011235",
        algorithm="HS256"
    )

    return jsonify(
        {
            'token':token,
            'message':'User logged in successfully',
        }
    ), 200
    
