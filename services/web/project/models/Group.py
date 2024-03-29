from datetime import datetime
from enum import Enum

from project import db
from project.models.User import User
from project.models.Schedule import Schedule
from project.models.Group_User import groups_users

from sqlalchemy.orm import relationship


class Group(db.Model):
    __tablename__ = "groups"

    class Privacy(Enum):
        PUBLIC = 'PUBLIC'
        PRIVATE = 'PRIVATE'

    class Difficulty(Enum):
        EASY = 'EASY'
        MIDDLE = 'MIDDLE'
        HARD = 'HARD'

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), nullable=False)
    privacy: Privacy = db.Column(db.Enum(Privacy), nullable=False)

    teacher = db.relationship('User', back_populates='my_groups')

    description: str = db.Column(db.String(512), nullable=True)
    difficulty: Difficulty = db.Column(db.Enum(Difficulty), nullable=True)
    capacity: int = db.Column(db.Integer, nullable=True)

    schedules = relationship("Schedule", cascade="all, delete-orphan")

    created_at: datetime = db.Column(db.Date, default=datetime.now())

    users = relationship('User', secondary='groups_users', back_populates='groups')

    # Claves Foraneas
    teacher_id: str = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name: str, privacy: Privacy, teacher: User, description: str = None, difficulty: Difficulty = None, capacity: int = None, schedules=[]):
        self.name = name
        self.privacy = privacy
        self.teacher = teacher
        self.description = description
        self.difficulty = difficulty
        self.capacity = capacity
        self.schedules = schedules

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'privacy': self.privacy.value,
            'teacher': self.teacher.to_dict_secondary(),
            'description': self.description,
            'difficulty': self.difficulty.value if self.difficulty else None,
            'capacity': self.capacity,
            'schedules': [schedule.to_dict() for schedule in self.schedules],
            'created_at': self.created_at,
            'users': [user.to_dict_secondary() for user in self.users]
        }

    def to_dict_secondary(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def add_user(self, user: User):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user: User):
        if user in self.users:
            self.users.remove(user)

    def add_schedule(self, schedule: Schedule):
        if schedule not in self.schedules:
            self.schedules.append(schedule)

    def remove_schedule(self, schedule: Schedule):
        if schedule in self.schedules:
            self.schedules.remove(schedule)

    @staticmethod
    def filter_paginated(page, per_page, privacy=None):
        query = Group.query.order_by(Group.created_at.asc())
        if privacy:
            query = query.filter_by(privacy=privacy)
        return query.paginate(page=page, per_page=per_page, error_out=False)
