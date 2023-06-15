from flask.cli import FlaskGroup

from project import app, db
from project.models.User import User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(username='carlos', password='zantana', gender=User.Gender.MALE, age=75))
    db.session.add(User(username='gustavo', password='cerati', gender=User.Gender.MALE, height=1.86, age=55))
    db.session.add(User(username='vanilla', password='ice', gender=User.Gender.MALE, age=55))
    db.session.add(User(username='dua', password='lipa', gender=User.Gender.FEMALE, height=1.73, age=27))
    db.session.commit()


if __name__ == "__main__":
    cli()
