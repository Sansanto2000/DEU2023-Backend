from enum import Enum

class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

class Clismo_User:
    def __init__(self, username:str, password:str, id:str=None, gender:Gender=None, weight:float=None, height:float=None, age:int=None):
        self.id:str = id
        self.username:str = username
        self.password:str = password
        self.gender:Gender = gender
        self.weight:float = weight
        self.height:float = height
        self.age:int = age