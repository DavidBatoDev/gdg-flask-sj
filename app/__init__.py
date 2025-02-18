# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize SQLAlchemy without binding it to an app yet
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)

    # Initialize the app with the database
    db.init_app(app)

    # Import routes so they get registered with the app
    with app.app_context():
        from . import routes
        db.create_all()  # Create database tables for our models

    return app
