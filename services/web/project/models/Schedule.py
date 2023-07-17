from enum import Enum

from project import db
from project.models.Training import Training

class Schedule(db.Model):
    __tablename__ = "schedules"

    class Day(Enum):
        MONDAY = 'MONDAY'
        TUESDAY = 'TUESDAY'
        WEDNESDAY = 'WEDNESDAY'
        THURSDAY = 'THURSDAY'
        FRIDAY = 'FRIDAY'
        SATURDAY = 'SATURDAY'
        SUNDAY = 'SUNDAY'

    id: str = db.Column(db.Integer, primary_key=True)
    day: Day = db.Column(db.Enum(Day), nullable=False)
    starttime = db.Column(db.Time, nullable=False)
    endingtime = db.Column(db.Time, nullable=False)
    
    # Llave foranea para que un grupo conosca sus schedules
    schedule_id: str = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    
    # A cada Schedule le corresponde un Training
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=True)
    training = db.relationship(Training, uselist=False, cascade="all, delete-orphan", single_parent=True)
    #training = db.relationship("Training", uselist=False, back_populates="schedule", cascade="all, delete-orphan", single_parent=True)
    
    
    def __init__(self, day: Day, starttime, endingtime, training = None):
    #def __init__(self, day: Day, starttime, endingtime):
        self.day = day
        self.starttime = starttime
        self.endingtime = endingtime
        #self.training = training
    
    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day.value,
            'starttime': str(self.starttime),
            'endingtime': str(self.endingtime),
            #'training': self.training
        }
    
    