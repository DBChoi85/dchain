from flask import Flask
from .routes.acc import acc_api
from .routes.token import token_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(acc_api, url_prefix='/acc')
    app.register_blueprint(token_api, url_prefix='/token')
    return app
