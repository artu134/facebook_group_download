from database.base_orm import BaseORM
from message import Message

class FacebookORM(BaseORM):
    def __init__(self, db_url):
        super().__init__(db_url)
        #TODO create the database if it's not created yet

    def add_message(self, message_data):
        session = self.Session()

        # Check if a message with the same content already exists
        if not session.query(Message).filter_by(message=message_data['message']).first():
            new_message = Message(id=message_data['id'], message=message_data['message'], language=message_data.get('language'))
            session.add(new_message)
            session.commit()

        session.close()

    def read_by_filter(self, model, **filters):
        session = self.Session()
        result = session.query(model).filter_by(**filters).all()
        session.close()
        return result