from flask.cli import FlaskGroup

from project import app, db
from project.models.User import User
from project.models.Group import Group

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # Creacion de usuarios
    db.session.add(User(username='carlos', password='zantana', role=User.Role.TEACHER, 
                        gender=User.Gender.MALE, age=75))
    db.session.add(User(username='gustavo', password='cerati', role=User.Role.TEACHER, 
                        gender=User.Gender.MALE, height=1.86, age=55))
    db.session.add(User(username='vanilla', password='ice', role=User.Role.STUDENT, 
                        gender=User.Gender.MALE, age=55))
    db.session.add(User(username='dua', password='lipa', role=User.Role.STUDENT,
                        gender=User.Gender.FEMALE, height=1.73, age=27))
    
    # Creacion de grupos
    db.session.add(Group(name='ciclismo rapido', privacy=Group.Privacy.PUBLIC, description='Grupo centrado en la aceleracion del ritmo, que nadie te alcance.'))
    db.session.add(Group(name='ciclismo alter', privacy=Group.Privacy.PRIVATE, description='Ciclismo alternativo, conoce todo el potencial de la bicicleta.', difficulty='PAZ'))
    
    db.session.commit()


if __name__ == "__main__":
    cli()
