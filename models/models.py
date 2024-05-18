import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Date, Integer, String

database_path = os.environ['DATABASE_PATH']
db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
    with app.app_context():
        db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''

'''
Actor
a persistent actor entity, extends the base SQLAlchemy Model
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(180), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    short()
        short form representation of the Actor model
    '''

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    '''
    long()
        long form representation of the Actor model
    '''

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': []
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Tom Hanks'
            actor.update()
    '''

    def update(self):
        db.session.commit()



'''
Movie
a persistent actor entity, extends the base SQLAlchemy Model
'''


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(180), unique=True)
    release_date = Column(Date, nullable=False)
    
    def __init__(self, title=None, release_date=None):
        self.title = title
        self.release_date = release_date
    
    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.release_date,
        }

    '''
    long()
        long form representation of the Movie model
    '''

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.release_date,
            'actors': []
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'He Knows You're Alone'
            movie.update()
    '''

    def update(self):
        db.session.commit()
