from project import db
# from project.models.Schedule import Schedule
# Schedule

class Training(db.Model):
    __tablename__ = "trainings"

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), nullable=False)
    description: str = db.Column(db.String(512), nullable=True)
    
    # schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=True) #Definición de clave foranea 
    # schedule = db.relationship('Schedule', back_populates="training", single_parent=True, cascade="all,delete-orphan")

    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
