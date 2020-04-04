from .models import Cooler, User

import logging

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker


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
                clr = Cooler()
                clr.name = fixture["fields"]["name"]
                clr.description = fixture["fields"]["description"]
                self.session.add(clr)
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
            result = and_(result, condition) if result else condition
        return self.session.query(Cooler).filter(result).first()

    def get_user(self, id=None, username=None, password=None):
        result = None
        if id is not None:
            result = User.id == id
        if username is not None:
            condition = User.username == username
            result = and_(result, condition) if result else condition 
        if password is not None:
            condition = User.password == password
            result = and_(result, condition) if result else condition
        return self.session.query(User).filter(result).first()
