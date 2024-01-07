from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True)
    message = Column(String)
    group_id = Column(String)
    language = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Message(id='{self.id}', group_id='{self.group_id}', message='{self.message}', language='{self.language}')>"
