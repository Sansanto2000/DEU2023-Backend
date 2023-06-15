from enum import Enum

from project import db

class User(db.Model):
    __tablename__ = "users"

    class Role(Enum):
        TEACHER = 'TEACHER'
        STUDENT = 'STUDENT'
    
    class Gender(Enum):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        OTHER = 'OTHER'
    
    id:str = db.Column(db.Integer, primary_key=True)
    username:str = db.Column(db.String(100), nullable=False)
    password:str = db.Column(db.String(100), nullable=False)
    rol:Role = db.Column(db.Enum(Role), nullable=False)
    gender:Gender = db.Column(db.Enum(Gender), nullable=True)
    weight:float = db.Column(db.Float, nullable=True)
    height:float = db.Column(db.Float, nullable=True)
    age:int = db.Column(db.Integer, nullable=True)

    def __init__(self, username:str, password:str, role:Role, gender:Gender=None, weight:float=None, 
                 height:float=None, age:int=None):
        self.username = username
        self.password = password
        self.role = role
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
