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

    def __init__(self, name: str, privacy: Privacy, description: str = None, difficulty: Difficulty = None, capacity: int = None, schedules = None):
        self.name = name
        self.privacy = privacy
        self.description = description
        self.difficulty = difficulty
        self.capacity = capacity
        self.schedules = schedules
