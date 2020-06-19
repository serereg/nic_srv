import logging
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Cooler, Session, User


class DBClient:
    def __init__(self, dsn, db):
        self.db = db
        self.dsn = dsn

    def connect(self):
        # await self.db.set_bind(self.dsn)
        # await self.db.gino.create_all()
        engine = create_engine(self.dsn)
        self.db.metadata.create_all(engine)

        self.db.metadata.bind = engine        
        DBSession = sessionmaker()
        self.session = DBSession(bind=engine)

    def close(self):
        self.db.pop_bind().close()

    def add_fixtures(self, fixtures):
        for fixture in fixtures:
            try:
                record = fixture["model"](**fixture["fields"])
                self.session.add(record)
                self.session.commit()
            except:
                self.session.rollback()
        
    def create_cooler(self, name, description=None):
        return Cooler.create(name=name, description=description)

    def get_coolers(self):
        return self.session.query(Cooler).all()

    def get_cooler(self, id=None, name=None):
        result = None
        if id is not None:
            result = Cooler.id == id
        if name is not None:
            condition = Cooler.name == name
            result = result & condition if result else condition
        return self.session.query(Cooler).filter(result).first()

    def remove_cooler(self, id=None, name=None):
        result = None
        if id is not None:
            result = Cooler.id == id
        if name is not None:
            condition = Cooler.name == name
            result = result & condition if result else condition
        coolers = self.session.query(Cooler).filter(result)
        coolers.delete()
        self.session.commit()

    def create_user(self, username, password):
        user = User(username=username, password=password)
        self.session.add(user)
        self.session.commit()

        return user

    def get_users(self):
        pass

    def get_user(self, id=None, username=None, password=None):
        result = None
        if id is not None:
            result = User.id == id
        if username is not None:
            condition = User.username == username
            result = result & condition if result else condition
        if password is not None:
            condition = User.password == password
            result = result & condition if result else condition
        print(username)
        if username == "Igor":
            return self.session.query(User).filter(result).first()
        else:
            return None
        # return self.session.query(User).filter(result).first()

    def remove_user(self, id=None, username=None, password=None):
        result = None
        if id is not None:
            result = User.id == id
        if username is not None:
            condition = User.username == username
            result = result & condition if result else condition 
        if password is not None:
            condition = User.password == password
            result = result & condition if result else condition
        users = self.session.query(User).filter(result)
        users.delete()
        self.session.commit()

    def create_session(self, user):
        while True:
            session = Session(user_id=user.id, token=str(uuid.uuid4()))
            try:
                self.session.add(session)
                self.session.commit()
                break
            except Exception as e:
                print(e)
                self.session.rollback()

        return session

    def get_sessions(self, user=None, token=None):
        pass

    def get_session(self, user=None, token=None):
        result = None
        if user is not None:
            result = Session.user_id == user.id
        if token is not None:
            condition = Session.token == token
            result = result & condition if result else condition  
        session = self.session.query(User).filter(result).first()
        return session
