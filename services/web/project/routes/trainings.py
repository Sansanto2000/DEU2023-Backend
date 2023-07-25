from flask import Blueprint, request, jsonify

from project import db
from project.models.User import User
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
    training = Training(name=name, description=description, teacher_id=teacher_id, exercises=exercises)
    
    # Generacion y agregado del training y sus exercises en la DB
    db.session.add(training)
    db.session.commit()
    
    return jsonify(training.to_dict()), 201

@trainings_api.route('/<int:training_id>/addExercise', methods=['PUT'])
def addExercise(training_id: int):
    # Endpoint para agregar un ejercicio a un entrenamiento determinado
    # Este espera varios parametros, uno por url y los demas por json:
    # # training_id: int <- por url, id del Training objetivo de la nueva incorporacion
    # # name: dict <- por json, nombre del ejercicio a agregar
    # # description: dict <- por json, descripcion del ejercicio a agregar
    # # speed: dict <- por json, speed del ejercicio a agregar
    # # heart_rate: dict <- por json, heart_rate del ejercicio a agregar
    # # duration: dict <- por json, duracion del ejercicio a agregar
    
    # Comprobacion de existencia del Training
    training: Training = Training.query.filter_by(id=training_id).first()
    if not training:
        return jsonify(error='No training for the given training_id'), 404
    
    # Obtencion de datos json y creacion del excercise
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    r1, r2 = check_excercise_dict(data)
    if r1:
        exercise: Exercise = r2
    else:
        return jsonify(error=f'Invalid exercises\'s item. {r2}'), 400    
    
    # Añadir Exercise creado al Training
    training.add_exercise(exercise=exercise)
    
    # Subida de los cambios a la db
    db.session.commit()

    return '', 204

@trainings_api.route('/<int:training_id>/removeExercise', methods=['PUT'])
def removeExercise(training_id: int):
    # Endpoint para quitar un ejercicio a un entrenamiento determinado
    # Este espera 2 parametros, uno por url y otro por json:
    # # training_id: int <- por url, id del Training objetivo del desenlazado
    # # exercise_id: int <- id del ejercicio que se pretende borrar
    
    # Comprobacion de existencia del Training
    training: Training = Training.query.filter_by(id=training_id).first()
    if not training:
        return jsonify(error='No training for the given training_id'), 404
    
    # Obtencion de datos json
    data = request.get_json()
    if not data:
        return jsonify(error='Missing JSON data'), 400
    
    exercise_id_str = data['exercise_id']
    if not exercise_id_str:
        return jsonify(error='exercise_id attribute cannot be null'), 400
    if not isinstance(exercise_id_str, int):
        return jsonify(error='Invalid exercise_id. exercise_id must be an integer value.'), 400
    exercise_id = int(exercise_id_str)
    exercise: Exercise = Exercise.query.filter_by(id=exercise_id).first()
    if not exercise:
        return jsonify(error='Invalid exercise_id. The given id does not correspond to any exercise'), 400
    elif not exercise in training.exercises:
        return jsonify(error='Invalid exercise_id. The given exercise was not in the exercises list of the given Training'), 400
    
    # Añadir usuario al grupo
    training.remove_exercise(exercise=exercise)
    db.session.delete(exercise)
    
    # Subida de los cambios a la db
    db.session.commit()

    return '', 204
