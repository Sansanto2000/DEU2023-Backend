from enum import Enum

class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

class User:
    def __init__(self, id:str, username:str, password:str, gender:Gender=None, weight:float=None, height:float=None, age:int=None):
        self.id:str = id
        self.username:str = username
        self.password:str = password
        self.gender:Gender = gender
        self.weight:float = weight
        self.height:float = height
        self.age:int = age
        
    def to_JSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'gender': self.gender,
            'weight': self.weight,
            'height': self.height,
            'age': self.age,
        }