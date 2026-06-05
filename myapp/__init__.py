import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from .routes.acc import acc_api
from .routes.token import token_api
from .routes.read_db import db_api
from .routes.did import did_api

def create_app():
    app = Flask(__name__)
    # -------------------------
    # 로그 설정
    # -------------------------
    # logs 디렉토리가 없으면 생성
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # 파일 로테이션 핸들러
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1_000_000,        # 1MB 넘으면 rotate
        backupCount=10,            # app.log.1 ~ app.log.10 보관
        encoding='utf-8'
    )

    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)

    # Flask app logger에 핸들러 추가
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # -------------------------
    # Blueprint 등록
    # -------------------------
    app.register_blueprint(acc_api, url_prefix='/acc')
    app.register_blueprint(token_api, url_prefix='/token')
    app.register_blueprint(db_api, url_prefix='/read_db')
    app.register_blueprint(did_api, url_prefix='/did')
    return app
