from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User
from project.models.Group import Group
from project.models.Training import Training
from project.models.Schedule import Schedule

schedules_api = Blueprint('schedules', __name__)


@schedules_api.route('/<int:schedule_id>', methods=['GET'])
def get(schedule_id: int):
    # Comprobacion existencia del entrenamiento en la DB
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify(error='No schedule for the given id'), 404

    return jsonify(schedule.to_dict()), 200


@schedules_api.route('/<int:schedule_id>/setTrainingId', methods=['PUT'])
def setTraining(schedule_id: int):
    # Comprobacion existencia del Schedule en la DB
    schedule: Schedule = Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify(error='No schedule for the given id'), 404

    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400

    # Comprobacion de existencia del training
    training_id_str = data['training_id']
    if not training_id_str:
        return jsonify(error='training attribute cannot be null'), 400
    if not isinstance(training_id_str, int):
        return jsonify(error='Invalid training_id. training_id must be an integer value.'), 400
    training_id = int(training_id_str)
    training: Training = Training.query.filter_by(id=training_id).first()
    if not training:
        return jsonify(error='Invalid training_id. The given id does not correspond to any training'), 400

    # Comprobacion de existencia y autoridad del usuario profesor
    teacher_id_str = data['teacher_id']
    if not teacher_id_str:
        return jsonify(error='teacher_id attribute cannot be null'), 400
    if not isinstance(teacher_id_str, int):
        return jsonify(error='Invalid teacher_id. teacher_id must be an integer value.'), 400
    teacher_id = int(teacher_id_str)
    teacher: User = User.query.filter_by(id=teacher_id).first()
    if not teacher:
        return jsonify(error='Invalid teacher_id. The given id does not correspond to any user'), 400
    if not teacher:
        return jsonify(error='No user for the given teacher_id'), 404
    elif teacher.role != User.Role.TEACHER:
        return jsonify(error='This user is not a teacher, therefore she cannot modifi it'), 404
    elif schedule.group.teacher != teacher:
        return jsonify(error='This user is not a teacher of the group of the indicated schedule, therefore she cannot modifi it.'), 404

    # Realizar modificacion del atributo training de la DB
    schedule.training = training

    # Subida de los cambios a la db
    db.session.commit()

    return jsonify(schedule.to_dict()), 200
