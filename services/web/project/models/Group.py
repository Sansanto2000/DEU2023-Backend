from datetime import datetime
from enum import Enum

from project import db

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
    description: str = db.Column(db.String(512), nullable=True)
    difficulty: Difficulty = db.Column(db.Enum(Difficulty), nullable=True)
    capacity: int = db.Column(db.Integer, nullable=True)
    schedules = relationship("Schedule", cascade="all, delete-orphan")
    created_at: datetime = db.Column(db.Date, default=datetime.now())

    def __init__(self, name: str, privacy: Privacy, description: str = None, difficulty: Difficulty = None, capacity: int = None, schedules = []):
        self.name = name
        self.privacy = privacy
        self.description = description
        self.difficulty = difficulty
        self.capacity = capacity
        self.schedules = schedules
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'privacy': self.privacy.value,
            'description': self.description,
            'difficulty': self.difficulty.value if self.difficulty else None,
            'capacity': self.capacity,
            'schedules': [schedule.to_dict() for schedule in self.schedules],
            'created_at': self.created_at
        }
    
    @staticmethod
    def filter_paginated(page, per_page, privacy=None):
        query = Group.query.order_by(Group.created_at.asc())
        if privacy:
            query = query.filter_by(privacy=privacy)
        return query.paginate(page=page, per_page=per_page, error_out=False)

