from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app