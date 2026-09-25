from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, request, current_app
from functools import wraps
import jwt
db = SQLAlchemy()
migrate =Migrate()

def dec(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error':'Invalid request'}), 401
        if "Bearer" not in auth_header:
            return jsonify({'error':'Invalid request'}), 401
        token = auth_header.split("Bearer ")
        token = token[1]

        try:
            decoded = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
            user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'Login Session Expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error':str(e)}), 401
        return f(*args, user_id=user_id, **kwargs)
    return wrapper