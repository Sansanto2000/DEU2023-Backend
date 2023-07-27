from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User
from project.models.Group import Group
from project.models.Schedule import Schedule
from project.models.Training import Training
from project.models.Invitation import Invitation

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

    training_id_str = schema['training_id'] # Retocar por Training Id
    training = None
    if training_id_str:
        training = Training.query.filter_by(id=training_id_str).first()
        if not training:
            return False, f'No training for the training_id={training_id_str}'

    return True, Schedule(day=day, starttime=starttime, endingtime=endingtime, training=training)

@groups_api.route('/create', methods=['POST'])
def create():
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400

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

@groups_api.route('/<int:group_id>/addUser', methods=['PUT'])
def addUser(group_id: int):
    # Endpoint para enlazar un usuario con un grupo determinado
    # Este espera 2 parametros de tipo int dentro de un parametro de tipo json:
    # # group_id: int <- id del grupo objetivo de la nueva incorporacion
    # # user_id: int <- id del usuario que se pretende incorporar al grupo
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400

    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    user_id_str = data['user_id']
    if not user_id_str:
        return jsonify(error='user_id attribute cannot be null'), 400
    if not isinstance(user_id_str, int):
        return jsonify(error='Invalid user_id. user_id must be an integer value.'), 400
    user_id = int(user_id_str)
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='Invalid user_id. The given id does not correspond to any user'), 400
    
    # Añadir usuario al grupo
    group.add_user(user)
    
    # Subida de los cambios a la db
    db.session.commit()

    return '', 204

@groups_api.route('/<int:group_id>/removeUser', methods=['PUT'])
def removeUser(group_id: int):
    # Endpoint para desenlazar un usuario con un grupo determinado
    # Este espera 2 parametros de tipo int dentro de un parametro de tipo json:
    # # group_id: int <- id del grupo objetivo del desenlazado
    # # user_id: int <- id del usuario que se pretende quitar del grupo
    
    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    user_id_str = data['user_id']
    if not user_id_str:
        return jsonify(error='user_id attribute cannot be null'), 400
    if not isinstance(user_id_str, int):
        return jsonify(error='Invalid user_id. user_id must be an integer value.'), 400
    user_id = int(user_id_str)
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='Invalid user_id. The given id does not correspond to any user'), 400
    
    # Añadir usuario al grupo
    group.remove_user(user)
    
    # Subida de los cambios a la db
    db.session.commit()

    return '', 204

@groups_api.route('/<int:group_id>/delete', methods=['DELETE'])
def delete(group_id: int):
    # Endpoint para borrar un grupo
    # El borrado solo lo puede realizar el profesor titular del respectivo grupo
    # Este espera 2 parametros cada uno atravez de cierta via:
    # - group_id: int <- Se espera mediante la url, hace referencia al id del grupo que se pretende borrar
    # - teacher_id: int <- Se envia mediante json, hace referencia al id del usuario que pretende realizar el borrado
    
    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    # Comprobacion de existencia y autoridad del usuario profesor
    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any teacher'), 400
    if not teacher:
        return jsonify(error='No user for the given teacher_id'), 404
    elif teacher.role != User.Role.TEACHER:
        return jsonify(error='This user is not a teacher, therefore she cannot delete groups'), 404
    elif group.teacher != teacher:
        return jsonify(error='This user is not a teacher of the indicated group, therefore she cannot delete it.'), 404
    
    # Borrar grupo de la DB
    db.session.delete(group)
    
    # Subida de los cambios a la db
    db.session.commit()
    
    return jsonify(group.to_dict()), 204

# @groups_api.route('/<int:group_id>/trainings', methods=['GET'])
# def get_trainings(group_id: int):
#     # Comprobacion existencia del usuario en la DB
#     group: Group = Group.query.filter_by(id=group_id).first()
#     if not group:
#         return jsonify(error='No group for the given id'), 404
    
#     return jsonify(group.to_dict()), 200

@groups_api.route('/<int:group_id>/addSchedule', methods=['PUT'])
def addSchedule(group_id: int):
    # Endpoint para enlazar un schedule con un grupo determinado
    # Este espera 3 parametros de tipo int, uno via url y dos via json:
    # # group_id: int <- id del grupo objetivo de la nueva incorporacion
    # # teacher_id: int <- hace referencia al id del usuario que pretende realizar el borrado
    # # schedule: dict <- datos del schedule que se pretende incorporar al grupo
    # # # day: enum <- MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY'
    # # # starttime: datatime, // Format %H:%M:%S
    # # # endingtime: datatime, // Format %H:%M:%S
    # # # training_id: int // (Optional) Valor id de training, sino se autoasigna null
    
    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id, role=User.Role.TEACHER).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any teacher'), 400
    elif group.teacher_id != teacher_id:
        return jsonify(error='Invalid teacher_id. The given teacher_id does not correspond to the teacher of the group in question'), 400
    
    schedule_dict = data['schedule']
    schedule = None
    if isinstance(schedule_dict, dict):
        r1, r2 = check_schedul_dict(schedule_dict)
        if r1:
            schedule = r2
        else:
            return jsonify(error=f'Invalid schedule\'s item. {r2}'), 400               
    else:
        return jsonify(error='Invalid schedules. Schedules must be a dict.'), 400
    
    # Añadir Scheduele al grupo
    group.add_schedule(schedule=schedule)
    
    # Subida de los cambios a la db
    db.session.commit()

    return jsonify(schedule.to_dict()), 200

@groups_api.route('/<int:group_id>/removeSchedule', methods=['PUT'])
def removeSchedule(group_id: int):
    # Endpoint para desenlazar un usuario con un grupo determinado
    # Este espera 3 parametros de tipo int, uno en la url y dos en json:
    # # group_id: int <- id del grupo objetivo del desenlazado
    # # teacher_id: int <- id del usuario profesor del del grupo
    # # schedule_id: int <- id del Schedule que se pretende quitar del grupo
    
    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id, role=User.Role.TEACHER).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any teacher'), 400
    elif group.teacher_id != teacher_id:
        return jsonify(error='Invalid teacher_id. The given teacher_id does not correspond to the teacher of the group in question'), 400
    
    schedule_id_str = data['schedule_id']
    if not schedule_id_str:
        return jsonify(error='schedule_id attribute cannot be null'), 400
    if not isinstance(schedule_id_str, int):
        return jsonify(error='Invalid schedule_id. schedule_id must be an integer value.'), 400
    schedule_id = int(schedule_id_str)
    schedule: Schedule = Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify(error='Invalid schedule_id. The given id does not correspond to any schedule'), 400
    elif not schedule in group.schedules:
        return jsonify(error='Invalid schedule_id. The given id does not correspond to any schedule of the group'), 400
            
    # Quitar Schedule del grupo y borrar Schedule de la DB
    group.remove_schedule(schedule)
    db.session.delete(schedule)
    
    # Subida de los cambios a la db
    db.session.commit()

    return '', 204

@groups_api.route('/<int:group_id>/generateInvitationForUser/<int:destination_user_id>', methods=['POST'])
def generateInvitationForUser(group_id: int, destination_user_id: int):
    # Endpoint para generar una invitacion al grupo a un usuario:
    # # group_id: int <- id del grupo objetivo del desenlazado
    # # destination_user_id: int <- id del Schedule que se pretende agregar
    # # teacher_id: int <- id del usuario profesor del del grupo
    
    # Comprobacion de existencia del grupo
    group: Group = Group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify(error='No group for the given group_id'), 404
    
    # Comprobacion de existencia del usuario
    destination_user: User = User.query.filter_by(id=destination_user_id).first()
    if not destination_user:
        return jsonify(error='No user for the given destination_user_id'), 404
    if destination_user in group.users:
        return jsonify(error='The specified user is already part of the specified group'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id, role=User.Role.TEACHER).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any teacher'), 400
    elif group.teacher_id != teacher_id:
        return jsonify(error='Invalid teacher_id. The given teacher_id does not correspond to the teacher of the group in question'), 400
    
    # Comprobacion de que no existen invitaciones identicas previamente creadas
    if Invitation.query.filter_by(id_group=group.id, id_user=destination_user.id).first():
        return jsonify(error='An invitation already exists for the indicated pair (group, user)'), 400
    
    # Creacion de la invitacion
    invitation: Invitation = Invitation(group=group, user=destination_user)
    
    # Generacion y agregado de la invitacion en la DB
    db.session.add(invitation)
    db.session.commit()

    return jsonify(invitation.to_dict()), 201