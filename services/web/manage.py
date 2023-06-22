from flask.cli import FlaskGroup

from project import app, db
from project.models.User import User
from project.models.Group import Group
from project.models.Schedule import Schedule

from datetime import time

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # Creacion de usuarios
    db.session.add(
        User(username='carlos', password='zantana', role=User.Role.TEACHER, gender=User.Gender.MALE, age=75))
    db.session.add(
        User(username='gustavo', password='cerati', role=User.Role.TEACHER, gender=User.Gender.MALE, height=1.86, age=55))
    db.session.add(
        User(username='vanilla', password='ice', role=User.Role.STUDENT, gender=User.Gender.MALE, age=55))
    db.session.add(
        User(username='dua', password='lipa', role=User.Role.STUDENT, gender=User.Gender.FEMALE, height=1.73, age=27))

    # Creacion de grupos
    schedules = [
        Schedule(day=Schedule.Day.MONDAY, starttime=time(8, 0, 0), endingtime=time(12, 0, 0)),
        Schedule(day=Schedule.Day.THURSDAY, starttime=time(16, 0, 0), endingtime=time(18, 0, 0))]
    db.session.add(
        Group(name='ciclismo rapido', privacy=Group.Privacy.PUBLIC, description='Grupo centrado en la aceleracion del ritmo, que nadie te alcance.', capacity=20, schedules=schedules))
    schedules = [
        Schedule(day=Schedule.Day.WEDNESDAY, starttime=time(17, 0, 0), endingtime=time(19, 0, 0)),
        Schedule(day=Schedule.Day.FRIDAY, starttime=time(16, 0, 0), endingtime=time(18, 0, 0))]
    db.session.add(
        Group(name='ciclismo alter', privacy=Group.Privacy.PRIVATE, description='Ciclismo alternativo, conoce todo el potencial de la bicicleta.', difficulty=Group.Difficulty.MIDDLE, schedules=schedules))
    schedules = [
        Schedule(day=Schedule.Day.MONDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.TUESDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.WEDNESDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.THURSDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.FRIDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.SATURDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0)),
        Schedule(day=Schedule.Day.SUNDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0))]
    db.session.add(
        Group(name='ciclismo hardcore', privacy=Group.Privacy.PUBLIC, description='Una vida, una bici, un destino.', difficulty=Group.Difficulty.HARD, capacity=10, schedules=schedules))
    schedules = [
        Schedule(day=Schedule.Day.SUNDAY, starttime=time(6, 0, 0), endingtime=time(10, 0, 0))]
    db.session.add(
        Group(name='grupo super exclusivo', privacy=Group.Privacy.PRIVATE, description='El grupo mas exclusivo de todos.', difficulty=Group.Difficulty.EASY, capacity=1, schedules=schedules))

    db.session.commit()


if __name__ == "__main__":
    cli()
