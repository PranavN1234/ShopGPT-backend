from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'shopGPT'
    app.config['SESSION_TYPE'] = 'filesystem'

    CORS(app, supports_credentials=True, origins="*")

    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app