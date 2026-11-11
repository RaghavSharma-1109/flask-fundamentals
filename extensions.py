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
            current_app.logger.info("Missing header")
            return jsonify({'error':'Invalid or missing token'}), 401
        auth_header = auth_header.split()
        if len(auth_header) != 2:
            current_app.logger.warning("Incorrect segments")
            return jsonify({'error':'Invalid or missing token'}), 401
        if auth_header[0] != "Bearer":
            current_app.logger.warning("Invalid Bearer")
            return jsonify({'error':'Invalid or missing token'}), 401
        token = auth_header[1]

        try:
            decoded = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
            user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            current_app.logger.info("Valid token expired")
            return jsonify({'error':'Invalid or missing token'}), 401
        except jwt.InvalidTokenError as e:
            current_app.logger.warning(type(e).__name__)
            return jsonify({'error':"Invalid or missing token"}), 401
        return f(*args, user_id=user_id, **kwargs)
    return wrapper