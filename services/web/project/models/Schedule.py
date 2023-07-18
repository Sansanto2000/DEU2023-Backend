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
    group_id: str = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    group = db.relationship('Group', back_populates='schedules')
    
    # A cada Schedule le corresponde un Training
    #training = relationship('User', secondary='groups_users', back_populates='groups')
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=True)
    training = db.relationship(Training, uselist=False)
    
    def __init__(self, day: Day, starttime, endingtime, training = None):
    #def __init__(self, day: Day, starttime, endingtime):
        self.day = day
        self.starttime = starttime
        self.endingtime = endingtime
        self.training = training
    
    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day.value,
            'starttime': str(self.starttime),
            'endingtime': str(self.endingtime),
            'group_id': self.group_id
        }
    
    