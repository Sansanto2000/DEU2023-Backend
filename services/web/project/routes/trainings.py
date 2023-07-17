from flask import Blueprint, request, jsonify

from project import db
from project.models.Training import Training

trainings_api = Blueprint('trainings', __name__)

@trainings_api.route('/<int:training_id>', methods=['GET'])
def get(training_id: int):
    # Comprobacion existencia del entrenamiento en la DB
    training = Training.query.filter_by(id=training_id).first()
    if not training:
        return jsonify(error='No training for the given id'), 404
    
    return jsonify(training.to_dict()), 200