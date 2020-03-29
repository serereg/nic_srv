from .models import Cooler

import logging

from sqlalchemy import create_engine
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
                logging.debug('commit')
                self.session.commit()
            except:
                self.session.rollback()
        
    def create_cooler(self, name, description=None):
        return Cooler.create(name=name, description=description)

    def get_coolers(self):
        return self.session.query(Cooler).all()

    def get_cooler(self, id=None, name=None):
        condition = True
        if id is not None:
            condition = condition and Cooler.id == id
        if name is not None:
            condition = condition and Cooler.name == name
        logging.info(name)
        return self.session.query(Cooler).filter(Cooler.name == name).first()
        # return self.session.query(Cooler).first()
