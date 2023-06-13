from enum import Enum
from flask_sqlalchemy import SQLAlchemy

# session_options={"expire_on_commit": False} =>
# would allow to manipulate out of date models
# after a transaction has been committed
# ! be aware that the above can have unintended side effects
db = SQLAlchemy()

class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

class User(db.Model):    
    __tablename__='clismo_users'
    
    id:str = db.Column(db.String(), primary_key=True)
    username:str = db.Column(db.String(100), nullable=False)
    password:str = db.Column(db.String(100), nullable=False)
    gender:Gender = db.Column(db.Enum(Gender), nullable=True)
    weight:float = db.Column(db.Float, nullable=True)
    height:float = db.Column(db.Float, nullable=True)
    age:int = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f"User {self.id}, {self.username}, {self.password}, {self.gender}, {self.weight}, {self.height}, {self.age}"
    
    # def __str__(self):
    #     return str(self.to_JSON)
    
    # def to_JSON(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'password': self.password,
    #         'gender': self.gender,
    #         'weight': self.weight,
    #         'height': self.height,
    #         'age': self.age,
    #     }
    
    # def __init__(self, id:str, username:str, password:str, gender:Gender=None, weight:float=None, height:float=None, age:int=None):
    #     self.id:str = id
    #     self.username:str = username
    #     self.password:str = password
    #     self.gender:Gender = gender
    #     self.weight:float = weight
    #     self.height:float = height
    #     self.age:int = age