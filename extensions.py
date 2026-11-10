from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, request, current_app
from functools import wraps
import jwt
db = SQLAlchemy()
migrate =Migrate()
# f ==> route
def dec(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error':'Invalid or missing token'}), 401
        auth_header = auth_header.split()
        if len(auth_header) != 2:
            return jsonify({'error':'Invalid or missing token'}), 401
        if auth_header[0] != "Bearer":
            return jsonify({'error':'Invalid or missing token'}), 401
        token = auth_header[1]

        try:
            decoded = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
            user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'Invalid or missing token'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error':"Invalid or missing token"}), 401
        return f(*args, user_id=user_id, **kwargs)
    return wrapper