from flask import Flask

from .main import main

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['UPLOAD_FOLDER'] = '..\storage\model_data'

    app.register_blueprint(main)

    return app