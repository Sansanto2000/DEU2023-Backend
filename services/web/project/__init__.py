import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
CORS(app, origins=['http://localhost:3000/', 'https://clismo.vercel.app/'])
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


from project.routes.auth import auth_api
app.register_blueprint(auth_api, url_prefix='/auth')

from project.routes.users import users_api
app.register_blueprint(users_api, url_prefix='/users')

from project.routes.groups import groups_api
app.register_blueprint(groups_api, url_prefix='/groups')

from project.routes.trainings import trainings_api
app.register_blueprint(trainings_api, url_prefix='/trainings')

from project.routes.schedules import schedules_api
app.register_blueprint(schedules_api, url_prefix='/schedules')


@app.route("/")
def hello_world():
    return jsonify(hello="world")
