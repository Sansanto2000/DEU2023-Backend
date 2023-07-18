from flask import Blueprint, request, jsonify

from project import db
from project.models.Exercise import Exercise
from project.models.Training import Training

trainings_api = Blueprint('trainings', __name__)

def check_excercise_dict(schema: dict):
    # Validacion de atributos recibidos
    name = schema['name']
    if not name:
        return False, 'day attribute cannot be null'
    
    description = schema['description']
    if not description:
        return False, 'day attribute cannot be null'
        
    speed_str = schema['speed']
    if not speed_str:
        return False, 'speed attribute cannot be null'
    try:
        speed = float(speed_str)
    except ValueError:
        return False, 'Invalid speed. This has to be a float'
    
    heart_rate_str = schema['heart_rate']
    if not heart_rate_str:
        return False, 'heart_rate attribute cannot be null'
    try:
        heart_rate = float(heart_rate_str)
    except ValueError:
        return False, 'Invalid heart_rate. This has to be a float'
    
    duration_str = schema['duration']
    if not duration_str:
        return False, 'duration attribute cannot be null'
    try:
        duration = float(duration_str)
    except ValueError:
        return False, 'Invalid duration. This has to be a float'

    return True, Exercise(name=name, description=description, speed=speed, heart_rate=heart_rate, duration=duration)
    

@trainings_api.route('/<int:training_id>', methods=['GET'])
def get(training_id: int):
    # Comprobacion existencia del entrenamiento en la DB
    training = Training.query.filter_by(id=training_id).first()
    if not training:
        return jsonify(error='No training for the given id'), 404
    
    return jsonify(training.to_dict()), 200

@trainings_api.route('/create', methods=['POST'])
def create():
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    name = data['name']
    if not name:
        return jsonify(error='name attribute cannot be null'), 400
    
    description = data['description']
    if not description:
        return jsonify(error='description attribute cannot be null'), 400
    
    exercises_str = data['exercises']
    exercises = []
    if isinstance(exercises_str, list):
        for exercise_str in exercises_str:
            r1, r2 = check_excercise_dict(exercise_str)
            if r1:
                exercises.append(r2) 
            else:
                return jsonify(error=f'Invalid exercises\'s item. {r2}'), 400               
    else:
        return jsonify(error='Invalid exercises. exercises must be a list.'), 400
    
    # Creacion del Training
    training = Training(name=name, description=description, exercises=exercises)
    
    # Generacion y agregado del training y sus exercises en la DB
    db.session.add(training)
    db.session.commit()
    
    return jsonify(training.to_dict()), 201