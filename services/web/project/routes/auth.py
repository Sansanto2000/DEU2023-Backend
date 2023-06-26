from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User

auth_api = Blueprint('auth', __name__)


@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify(error='Missing JSON data'), 400
    # Recepcion de campos obligatorios
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify(error='Missing username or password'), 400

    # Comprobacion existencia del usuario en la DB
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify(error='Invalid username or password'), 401

    return jsonify({'message': 'Login successful', 'id': user.id}), 200


@auth_api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400

    # Recepcion de campos obligatorios
    username = data.get('username')
    password = data.get('password')
    role_str = data.get('role')
    if not username or not password or not role_str:
        return jsonify(error='Missing username, password, or role'), 400
    try:
        role = User.Role(role_str)
    except ValueError:
        valid_roles = [g.value for g in User.Role]
        return jsonify(error=f'Invalid role. Valid values are: {valid_roles}'), 400

    # Recepcion de campos opcionales
    gender_str = data.get('gender')
    weight_str = data.get('weight')
    height_str = data.get('height')
    age_str = data.get('age')

    gender = None
    if gender_str:
        try:
            gender = User.Gender(gender_str)
        except ValueError:
            valid_genders = [g.value for g in User.Gender]
            return jsonify(error=f'Invalid gender. Valid values are: {valid_genders}'), 400

    weight = None
    if weight_str:
        if not isinstance(weight_str, float):
            return jsonify(error='Invalid weight. Weight must be a float value.'), 400
        weight = float(weight_str)

    height = None
    if height_str:
        if not isinstance(height_str, float):
            return jsonify(error='Invalid height. Height must be a float value.'), 400
        height = float(height_str)

    age = None
    if age_str:
        if not isinstance(age_str, int):
            return jsonify(error='Invalid age. Age must be an integer value.'), 400
        age = int(age_str)

    # Comprobacion de valides de los campos en la DB
    if User.query.filter_by(username=username).first():
        return jsonify(error='The username is already taken'), 409

    # Generacion y agregado del usuario en la DB
    user = User(username=username, password=password, role=role, gender=gender, weight=weight, height=height, age=age)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201
