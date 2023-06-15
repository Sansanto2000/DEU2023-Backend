from enum import Enum

from project import db

class Group(db.Model):
    __tablename__ = "groups"
    
    class Privacy(Enum):
        PUBLIC ='PUBLIC'
        PRIVATE ='PRIVATE'
    
    id:str = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(128), nullable=False)
    privacy:Privacy = db.Column(db.Enum(Privacy), nullable=False)
    description:str = db.Column(db.String(512), nullable=True)
    difficulty:str = db.Column(db.String(128), nullable=True)

    def __init__(self, name:str, privacy:Privacy, description:str=None, difficulty:str=None):
        self.name = name
        self.privacy = privacy
        self.description = description
        self.difficulty = difficulty
