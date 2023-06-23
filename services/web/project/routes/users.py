from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User

users_api = Blueprint('users', __name__)

@users_api.route('/<int:user_id>', methods=['GET'])
def get(user_id: int):
    # Comprobacion existencia del usuario en la DB
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    return jsonify(user.to_dict()), 200

@users_api.route('/update/<int:user_id>', methods=['PUT'])
def update(user_id: int):
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='There is no user for the given id'), 404
    
    # Obtencion de datos json y modificacion de los campos
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
        
    try:
        username = data['username']
        if not username:
            return jsonify(error='username attribute cannot be null'), 400
        user.username = username
    except KeyError:
        pass

    try:
        password = data['password']
        if not password:
            return jsonify(error='password attribute cannot be null'), 400
        user.password = password
    except KeyError:
        pass

    try:
        role_str = data['role']
        if not role_str:
            return jsonify(error='role attribute cannot be null'), 400
        try:
            role = User.Role(role_str)
            user.role = role
        except ValueError:
            valid_roles = [g.value for g in User.Role]
            return jsonify(error=f'Invalid role. Valid values are: {valid_roles}'), 400
    except KeyError:
        pass

    try:
        gender_str = data['gender']
        gender = None
        if gender_str:
            try:
                gender = User.Gender(gender_str)
            except ValueError:
                valid_genders = [g.value for g in User.Gender]
                return jsonify(error=f'Invalid gender. Valid values are: {valid_genders}'), 400
        user.gender = gender
    except KeyError:
        pass

    try:
        weight_str = data['weight']
        weight = None
        if weight_str:
            if not isinstance(weight_str, float):
                return jsonify(error='Invalid weight. Weight must be a float value.'), 400
            weight = float(weight_str)
        user.weight = weight
    except KeyError:
        pass

    try:
        height_str = data['height']
        height = None
        if height_str:
            if not isinstance(height_str, float):
                return jsonify(error='Invalid height. Height must be a float value.'), 400
            height = float(height_str)
        user.height = height
    except KeyError:
        pass

    try:
        age_str = data['age']
        age = None
        if age_str:
            if not isinstance(age_str, int):
                return jsonify(error='Invalid age. Age must be an integer value.'), 400
            age = int(age_str)
        user.age = age
    except KeyError:
        pass
    
    # Actualizacion de los cambios en la DB
    db.session.commit()

    return jsonify(user.to_dict()), 200
