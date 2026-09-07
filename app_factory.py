from extensions import db
from items import items_bp
from model import Item
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///items.db'
    db.init_app(app)

    app.register_blueprint(items_bp)

    return app