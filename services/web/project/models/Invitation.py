from project import db
from project.models.User import User
from project.models.Group import Group
# Schedule

class Invitation(db.Model):
    __tablename__ = "invitations"

    id: str = db.Column(db.Integer, primary_key=True)
    
    id_group: str = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    group = db.relationship(Group, uselist=False)
    id_user: str = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User, uselist=False)
    
    accepted: bool = db.Column(db.Boolean, nullable=False)

    def __init__(self, group: Group, user: User):
        self.group = group
        self.user = user
        self.accepted = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_group': self.id_group,
            'id_user': self.id_user,
            'accepted': self.accepted
        }
        
    def accept(self):
        self.group.add_user(self.user)
        self.accepted = True
