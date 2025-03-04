from flask import Flask
from .config import Config

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import and register blueprints or routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app