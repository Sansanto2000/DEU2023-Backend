from flask import Blueprint, request, jsonify

from project import db
from project.models.Schedule import Schedule

schedules_api = Blueprint('schedules', __name__)

@schedules_api.route('/<int:schedule_id>', methods=['GET'])
def get(schedule_id: int):
    # Comprobacion existencia del entrenamiento en la DB
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify(error='No schedule for the given id'), 404
    
    return jsonify(schedule.to_dict()), 200