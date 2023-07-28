from enum import Enum
from datetime import datetime, timedelta

from project import db
from project.models.Group_User import groups_users

from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"

    class Role(Enum):
        TEACHER = 'TEACHER'
        STUDENT = 'STUDENT'

    class Gender(Enum):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        OTHER = 'OTHER'

    id: str = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(100), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)
    role: Role = db.Column(db.Enum(Role), nullable=False)
    gender: Gender = db.Column(db.Enum(Gender), nullable=True)
    weight: float = db.Column(db.Float, nullable=True)
    height: float = db.Column(db.Float, nullable=True)
    age: int = db.Column(db.Integer, nullable=True)
    groups = relationship('Group', secondary='groups_users', back_populates='users')
    my_groups = relationship("Group", back_populates='teacher')
    
    # Lista de schedules que el usuario realizo
    schedules_realized_list = relationship('RecordOfMade', cascade="all, delete-orphan", back_populates='user')

    def __init__(self, username: str, password: str, role: Role, gender: Gender = None, weight: float = None, height: float = None, age: int = None):
        self.username = username
        self.password = password
        self.role = role
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role.value,
            'gender': self.gender.value if self.gender else None,
            'weight': self.weight,
            'height': self.height,
            'age': self.age,
            'groups': [group.to_dict_secondary() for group in self.groups],
            'my_groups': [group.to_dict_secondary() for group in self.my_groups]
        }
    
    def to_dict_secondary(self):
        return {
            'id': self.id,
            'username': self.username
        }
        
    def getCompletedSchedulesId(self, days_lapse: int) -> list: 
        final_set: set = set(recordofmade.schedule.id for recordofmade in self.schedules_realized_list
                               if ((datetime.now() - recordofmade.realized_at) < timedelta(days=days_lapse)))
        return list(final_set)
    
    def getCompletedSchedulesRegister(self, days_lapse: int) -> list: 
        final_set: set = set(recordofmade for recordofmade in self.schedules_realized_list
                               if ((datetime.now() - recordofmade.realized_at) < timedelta(days=days_lapse)))
        return list(final_set)