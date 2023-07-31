from project import db


class Exercise(db.Model):
    __tablename__ = "exercises"

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), nullable=False)
    description: str = db.Column(db.String(512), nullable=True)
    speed: float = db.Column(db.Float, nullable=True)
    heart_rate: float = db.Column(db.Float, nullable=True)
    duration: float = db.Column(db.Float, nullable=True)

    # Claves Foranea para que cada entrenamiento sepa que ejercicios le corresponden
    training_id: str = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=True)

    def __init__(self, name: str, description: str, speed: float, heart_rate: float, duration: float):
        self.name = name
        self.description = description
        self.speed = speed
        self.heart_rate = heart_rate
        self.duration = duration

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'speed': self.speed,
            'heart_rate': self.heart_rate,
            'duration': self.duration,
        }
