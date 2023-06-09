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



@app.route("/")
def hello_world():
    return jsonify(hello="world")

# @app.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)


# @app.route("/media/<path:filename>")
# def mediafiles(filename):
#     return send_from_directory(app.config["MEDIA_FOLDER"], filename)


# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#     return """
#     <!doctype html>
#     <title>upload new File</title>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file><input type=submit value=Upload>
#     </form>
#     """
