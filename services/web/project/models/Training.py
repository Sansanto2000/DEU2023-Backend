from project import db
from project.models.Exercise import Exercise
# Schedule

class Training(db.Model):
    __tablename__ = "trainings"

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), nullable=False)
    description: str = db.Column(db.String(512), nullable=True)
    
    exercises = db.relationship("Exercise", cascade="all, delete-orphan")

    def __init__(self, name: str, description: str, exercises = []):
        self.name = name
        self.description = description
        self.exercises = exercises
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'exercises': [exercise.to_dict() for exercise in self.exercises],
        }
        
    def add_exercise(self, exercise: Exercise):
        if exercise not in self.exercises:
            self.exercises.append(exercise)
    
    def remove_exercise(self, exercise: Exercise):
        if exercise in self.exercises:
            self.exercises.remove(exercise)
