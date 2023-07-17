from flask.cli import FlaskGroup

from project import app, db
from project.models.User import User
from project.models.Group import Group
from project.models.Schedule import Schedule
from project.models.Training import Training
from project.models.Exercise import Exercise

from datetime import time
from copy import copy

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    
    # Creacion de entrenamientos cada cual con sus respectivos ejercicios
    exercises = [
        Exercise(name="curl de biceps", description= "...", speed= 2.0, heart_rate= 90.0, duration= 30.0),
        Exercise(name="flexiones", description= "...", speed= 4.0, heart_rate= 90.0, duration= 30.0),
        Exercise(name="bicicleta", description= "...", speed= 7.0, heart_rate= 90.0, duration= 100.0)]
    training_arms = Training(name="Brazos", description="Entrenamiento de brazos", exercises=exercises)
    exercises = [
        Exercise(name="sentadillas", description= "...", speed= 3.0, heart_rate= 120.0, duration= 30.0),
        Exercise(name="bicicleta", description= "...", speed= 7.0, heart_rate= 90.0, duration= 400.0)]
    training_legs = Training(name="Piernas", description="Entrenamiento de piernas", exercises=exercises)
    exercises = [
        Exercise(name="abdominales", description= "...", speed= 3.0, heart_rate= 120.0, duration= 30.0),
        Exercise(name="bicicleta", description= "...", speed= 7.0, heart_rate= 90.0, duration= 300.0)]
    training_core = Training(name="Core", description="Entrenamiento de core", exercises=exercises)
    
    # Creacion de usuarios
    user1 = User(username='carlos', password='zantana', role=User.Role.TEACHER, gender=User.Gender.MALE, age=75)
    db.session.add(user1)
    user2 = User(username='gustavo', password='cerati', role=User.Role.TEACHER, gender=User.Gender.MALE, height=1.86, age=55)
    db.session.add(user2)
    user3 = User(username='vanilla', password='ice', role=User.Role.STUDENT, gender=User.Gender.MALE, age=55)
    db.session.add(user3)
    user4 = User(username='dua', password='lipa', role=User.Role.STUDENT, gender=User.Gender.FEMALE, height=1.73, age=27)
    db.session.add(user4)

    # Creacion de grupos
    schedules = [
        Schedule(day=Schedule.Day.MONDAY, starttime=time(8, 0, 0), endingtime=time(12, 0, 0), training=training_legs),
        Schedule(day=Schedule.Day.THURSDAY, starttime=time(16, 0, 0), endingtime=time(18, 0, 0), training=training_legs)]
    group1 = Group(name='ciclismo rapido', privacy=Group.Privacy.PUBLIC, teacher=user1, description='Grupo centrado en la aceleracion del ritmo, que nadie te alcance.', capacity=20, schedules=schedules)
    group1.add_user(user3)
    group1.add_user(user4)
    db.session.add(group1)
    schedules = [
        Schedule(day=Schedule.Day.WEDNESDAY, starttime=time(17, 0, 0), endingtime=time(19, 0, 0), training=training_core),
        Schedule(day=Schedule.Day.FRIDAY, starttime=time(16, 0, 0), endingtime=time(18, 0, 0), training=training_core)]
    group2 = Group(name='ciclismo alter', privacy=Group.Privacy.PRIVATE, teacher=user2, description='Ciclismo alternativo, conoce todo el potencial de la bicicleta.', difficulty=Group.Difficulty.MIDDLE, schedules=schedules)
    group2.add_user(user4)
    db.session.add(group2)
    schedules = [
        Schedule(day=Schedule.Day.MONDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_legs),
        Schedule(day=Schedule.Day.TUESDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_core),
        Schedule(day=Schedule.Day.WEDNESDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_legs),
        Schedule(day=Schedule.Day.THURSDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_core),
        Schedule(day=Schedule.Day.FRIDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_legs),
        Schedule(day=Schedule.Day.SATURDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_core),
        Schedule(day=Schedule.Day.SUNDAY, starttime=time(7, 0, 0), endingtime=time(9, 0, 0), training=training_legs)]
    group3 = Group(name='ciclismo hardcore', privacy=Group.Privacy.PUBLIC, teacher=user2, description='Una vida, una bici, un destino.', difficulty=Group.Difficulty.HARD, capacity=10, schedules=schedules)
    db.session.add(group3)
    schedules = [
        Schedule(day=Schedule.Day.SUNDAY, starttime=time(6, 0, 0), endingtime=time(10, 0, 0), training=training_arms)]
    group4 = Group(name='grupo super exclusivo', privacy=Group.Privacy.PRIVATE, teacher=user1, description='El grupo mas exclusivo de todos.', difficulty=Group.Difficulty.EASY, capacity=1, schedules=schedules)
    group4.add_user(user3)
    db.session.add(group4)

    db.session.commit()


if __name__ == "__main__":
    cli()
