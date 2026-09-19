from extensions import db,migrate
from items import items_bp
from auth import user_bp
from model import Item,User
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///items.db'
    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(items_bp)
    app.register_blueprint(user_bp)

    return app