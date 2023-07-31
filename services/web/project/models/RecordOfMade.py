from datetime import datetime

from project import db
# from project.models.User import User
# from project.models.Schedule import Schedule


class RecordOfMade(db.Model):
    __tablename__ = "recordsofmade"

    id: str = db.Column(db.Integer, primary_key=True)

    user_id: str = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='schedules_realized_list')

    schedule_id: str = db.Column('schedule_id', db.Integer, db.ForeignKey('schedules.id'))
    schedule = db.relationship('Schedule', back_populates='realized_list')

    realized_at: datetime = db.Column('realized_at', db.DateTime, default=lambda: datetime.now())

    def __init__(self, user, schedule, realized_at: datetime = datetime.now()):
        self.user = user
        self.schedule = schedule
        self.realized_at = realized_at

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'schedule_id': self.schedule_id,
            'realized_at': self.realized_at,
        }
