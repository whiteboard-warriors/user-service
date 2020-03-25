from flask import Flask
from flask_cors import CORS
from flask_restplus import Api


def create_app():
    from users.api import api_ns

    app = Flask(__name__)
    CORS(app)
    api = Api(app, version='0.1', title="User API")
    from users.db import db, db_config
    app.config.update(db_config)
    db.init_app(app)

    app.db = db

    api.add_namespace(api_ns)

    return app
