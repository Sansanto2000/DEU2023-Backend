from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User
from project.models.Group import Group
from project.models.Schedule import Schedule

from datetime import datetime

groups_api = Blueprint('groups', __name__)

@groups_api.route('/<int:group_id>', methods=['GET'])
def get(group_id: int):
    # Comprobacion existencia del usuario en la DB
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given id'), 404
    
    return jsonify(group.to_dict()), 200

@groups_api.route('/list', methods=['GET'])
def getlist():
    # Recepcion de parametros (Todos son opcionales, page y per_page tienen valores por defecto de no asignarse)
    params = request.args
    
    page_str = params.get("page", default=1)
    try:
        page: int = int(page_str)
    except (ValueError, TypeError):
        return jsonify(error='Invalid page. page must be an integer value.'), 400

    per_page_str = params.get("per_page", default=20) 
    try:
        per_page: int = int(per_page_str)
    except (ValueError, TypeError):
        return jsonify(error='Invalid per_page. per_page must be an integer value.'), 400
    
    privacy_str = params.get("privacy") 
    privacy: Group.Privacy = None
    if privacy_str:
        try:
            privacy = Group.Privacy(privacy_str)
        except ValueError:
            valid_privacies = [g.value for g in Group.Privacy]
            return jsonify(error=f'Invalid privacy. Valid values are: {valid_privacies}'), 400
    
    # Obtencion de los grupos requeridos
    groups = Group.filter_paginated(page=page, per_page=per_page, privacy=privacy)
    
    return jsonify([group.to_dict() for group in groups]), 200

def check_schedul_dict(schema: dict):
    # Validacion de atributos recibidos
    day_str = schema['day']
    if not day_str:
        return False, 'day attribute cannot be null'
    try:
        day = Schedule.Day(day_str)
    except ValueError:
        valid_days = [g.value for g in Schedule.Day]
        return False, f'Invalid day. Valid values are: {valid_days}'
    
    starttime_str = schema['starttime']
    if not starttime_str:
        return False, 'starttime attribute cannot be null'
    try:
        starttime = datetime.strptime(starttime_str, '%H:%M:%S').time()
    except ValueError:
        return False, 'Invalid starttime. Valid format is: %H:%M:%S'
    
    endingtime_str = schema['endingtime']
    if not endingtime_str:
        return False, 'endingtime attribute cannot be null'
    try:
        endingtime = datetime.strptime(endingtime_str, '%H:%M:%S').time()
    except ValueError:
        return False, 'Invalid endingtime. Valid format is: %H:%M:%S'

    training = schema['training']
    # if not training:
    #     return False, 'training attribute cannot be null'

    return True, Schedule(day=day, starttime=starttime, endingtime=endingtime, training=training)
    

@groups_api.route('/create', methods=['POST'])
def create():
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    name: str = db.Column(db.String(128), nullable=False)

    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any user'), 400
    if teacher.role != User.Role.TEACHER:
        return jsonify(error=f'Invalid teacher_id. The given id belongs to a User who has the {User.Role.STUDENT} role, not {User.Role.TEACHER}.'), 400
    
    name = data['name']
    if not name:
        return jsonify(error='name attribute cannot be null'), 400

    privacy_str = data['privacy']
    if not privacy_str:
        return jsonify(error='privacy attribute cannot be null'), 400
    try:
        privacy = Group.Privacy(privacy_str)
    except ValueError:
        valid_privacies = [g.value for g in Group.Privacy]
        return jsonify(error=f'Invalid privacy. Valid values are: {valid_privacies}'), 400

    description = data['description']

    difficulty_str = data['difficulty']
    try:
        difficulty = Group.Difficulty(difficulty_str)
    except ValueError:
        valid_difficulties = [g.value for g in Group.Difficulty]
        return jsonify(error=f'Invalid difficulty. Valid values are: {valid_difficulties}'), 400
    
    capacity_str = data['capacity']
    capacity = None
    if capacity_str:
        if not isinstance(capacity_str, int):
            return jsonify(error='Invalid capacity. Capacity must be an integer value.'), 400
        capacity = int(capacity_str)

    schedules_str = data['schedules']
    schedules = []
    if isinstance(schedules_str, list):
        for schedul_str in schedules_str:
            r1, r2 = check_schedul_dict(schedul_str)
            if r1:
                schedules.append(r2) 
            else:
                return jsonify(error=f'Invalid schedules\'s item. {r2}'), 400               
    else:
        return jsonify(error='Invalid schedules. Schedules must be a list.'), 400
    # Creacion del Grupo
    group = Group(name=name, privacy=privacy, teacher=teacher, description=description, difficulty=difficulty, capacity=capacity, schedules=schedules)
    
    # Generacion y agregado del grupo y sus schedules en la DB
    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 200

# @groups_api.route('/<int:group_id>', methods=['DELETE'])
# def delete(group_id: int):
#     # Comprobacion de que el 
#     # Comprobacion existencia del usuario en la DB
#     group = Group.query.filter_by(id=group_id).first()
#     if not group:
#         return jsonify(error='No group for the given id'), 404
    
#     return jsonify(group.to_dict()), 200

# @groups_api.route('/update/<int:user_id>', methods=['PUT'])
# def update(user_id: int):
#     # Comprobacion existencia del usuario en la DB
#     user: User = User.query.filter_by(id=user_id).first()
#     if not user:
#         return jsonify(error='There is no user for the given id'), 404
    
#     # Obtencion de datos json y modificacion de los campos
#     data = request.get_json()
#     if not data:
#         return jsonify(error='Missing JSON data'), 400
        
#     try:
#         username = data['username']
#         if not username:
#             return jsonify(error='username attribute cannot be null'), 400
#         user.username = username
#     except KeyError:
#         pass

#     try:
#         password = data['password']
#         if not password:
#             return jsonify(error='password attribute cannot be null'), 400
#         user.password = password
#     except KeyError:
#         pass

#     try:
#         role_str = data['role']
#         if not role_str:
#             return jsonify(error='role attribute cannot be null'), 400
#         try:
#             role = User.Role(role_str)
#             user.role = role
#         except ValueError:
#             valid_roles = [g.value for g in User.Role]
#             return jsonify(error=f'Invalid role. Valid values are: {valid_roles}'), 400
#     except KeyError:
#         pass

#     try:
#         gender_str = data['gender']
#         gender = None
#         if gender_str:
#             try:
#                 gender = User.Gender(gender_str)
#             except ValueError:
#                 valid_genders = [g.value for g in User.Gender]
#                 return jsonify(error=f'Invalid gender. Valid values are: {valid_genders}'), 400
#         user.gender = gender
#     except KeyError:
#         pass

#     try:
#         weight_str = data['weight']
#         weight = None
#         if weight_str:
#             if not isinstance(weight_str, float):
#                 return jsonify(error='Invalid weight. Weight must be a float value.'), 400
#             weight = float(weight_str)
#         user.weight = weight
#     except KeyError:
#         pass

#     try:
#         height_str = data['height']
#         height = None
#         if height_str:
#             if not isinstance(height_str, float):
#                 return jsonify(error='Invalid height. Height must be a float value.'), 400
#             height = float(height_str)
#         user.height = height
#     except KeyError:
#         pass

#     try:
#         age_str = data['age']
#         age = None
#         if age_str:
#             if not isinstance(age_str, int):
#                 return jsonify(error='Invalid age. Age must be an integer value.'), 400
#             age = int(age_str)
#         user.age = age
#     except KeyError:
#         pass
    
#     # Actualizacion de los cambios en la DB
#     db.session.commit()

#     return jsonify(user.to_dict()), 200
