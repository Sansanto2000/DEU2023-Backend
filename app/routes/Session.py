from flask import Blueprint, jsonify

# Models
from models.UserModel import UserModel

api=Blueprint('session_blueprint', __name__)

@api.route('/')
def get_users():
    try:
        users=UserModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    return jsonify({'message':'Hola Mundo, ¿que tal estan de ese lado?'})