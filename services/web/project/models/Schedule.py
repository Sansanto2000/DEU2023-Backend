from enum import Enum

from project import db


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
    training: str = db.Column(db.String, nullable=True)
    # Claves foraneas
    _group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    
    def __init__(self, day: Day, starttime, endingtime, training = None):
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
            'training': self.training
        }
    
    