from flask import Flask, jsonify

from routes import init_routes

def create_app(test_config=None):

    # creates an application that is named after the name of the file
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "P4SSWORD1*_?"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@pgsql:5432/deudb"

    # initializing routes
    init_routes(app)

    return app