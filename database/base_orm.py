from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseORM:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add(self, obj):
        session = self.Session()
        session.add(obj)
        session.commit()
        session.close()

    def delete(self, model, identifier):
        session = self.Session()
        obj = session.query(model).get(identifier)
        if obj:
            session.delete(obj)
            session.commit()
        session.close()

    def update(self, model, identifier, updated_data):
        session = self.Session()
        obj = session.query(model).get(identifier)
        if obj:
            for key, value in updated_data.items():
                setattr(obj, key, value)
            session.commit()
        session.close()

    def read(self, model, identifier):
        session = self.Session()
        obj = session.query(model).get(identifier)
        session.close()
        return obj
