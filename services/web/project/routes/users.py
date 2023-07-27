from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User
from project.models.Schedule import Schedule
from project.models.Invitation import Invitation
from project.models.RecordOfMade import RecordOfMade

users_api = Blueprint('users', __name__)

@users_api.route('/<int:user_id>', methods=['GET'])
def get(user_id: int):
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    return jsonify(user.to_dict()), 200

@users_api.route('/<int:user_id>/invitations', methods=['GET'])
def getInvitations(user_id: int):
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    invitations: list = Invitation.query.filter_by(id_user=user.id).all()
    data = [invitation.to_dict() for invitation in invitations]
    return jsonify(data), 200

@users_api.route('/<int:user_id>/invitation/<int:invitation_id>/accept', methods=['PUT'])
def acceptInvitation(user_id: int, invitation_id: int):
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    # Comprobacion existencia de la invitacion en la DB
    invitation: Invitation = Invitation.query.filter_by(id=invitation_id).first()
    if not invitation:
        return jsonify(error='No invitation for the given id'), 404
    elif invitation.id_user != user.id:
        return jsonify(error='The indicated invitation does not belong to the specified user'), 404
    elif invitation.accepted:
        return jsonify(error='The indicated invitation has already been accepted previously'), 404
    
    # Aceptacion de la invitacion
    invitation.accept()
    
    # Actualizacion de los cambios en la DB
    db.session.commit()
    
    return jsonify(invitation.to_dict()), 200

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

@users_api.route('/<int:user_id>/schedules/completed', methods=['GET'])
def getCompletedSchedulesId(user_id: int):
    # Devuelve un listado con todos los schedules completados por el usuario dado un lapso de tiempo
    # # user_id: int <- url, id del grupo objetivo del desenlazado
    # # days_lapse: int <- json, cantidad de dias desde la realizacion para considerar un schedule como realizado
    
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    days_lapse_str = data['days_lapse']
    if not days_lapse_str:
        return jsonify(error='days_lapse attribute cannot be null'), 400
    elif not isinstance(days_lapse_str, int):
        return jsonify(error='Invalid days_lapse. days_lapse must be an integer value.'), 400
    days_lapse: int = int(days_lapse_str)
    if days_lapse < 0:
        return jsonify(error='Invalid days_lapse. days_lapse must be greater than or equal to 0'), 400
    
    # Obtiene el listado de los id de los schedules que el usuario realizo en el plazo de tiempo indicado
    ids_list = user.getCompletedSchedulesId(days_lapse=days_lapse)
    
    return jsonify({"ids_of_realized_schedules": ids_list}), 200

@users_api.route('/<int:user_id>/schedule/<int:schedule_id>/complete', methods=['PUT'])
def completeSchedule(user_id: int, schedule_id: int):
    # Comprobacion existencia del usuario en la DB
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(error='No user for the given id'), 404
    
    # Comprobacion existencia del schedule en la DB
    schedule: Schedule = Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify(error='No schedule for the given id'), 404
    elif not schedule.group in user.groups:
        return jsonify(error='The specified schedule does not belong to any group in which the user is subscribed'), 404
    
    # Agregar entrada de realizacion del schedule por parte del usuario
    recordofmade: RecordOfMade = RecordOfMade(user=user, schedule=schedule)
    
    # Actualizacion de los cambios en la DB
    db.session.add(recordofmade)
    db.session.commit()
    
    return jsonify(recordofmade.to_dict()), 200
