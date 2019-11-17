from backend import db
import datetime
from backend.models.user import User
from backend.models.message import Message


class Conversation(db.Model):
    conversation_id = db.Column(db.Integer, primary_key=True)
    trainer_uuid = db.Column(db.String, unique=True, nullable=False)
    user_uuid = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    messages = db.relationship("Message")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_trainer_uuid(cls, trainer_uuid):
        return cls.query.filter_by(trainer_uuid=trainer_uuid).first()

    @classmethod
    def get_user_by_user_uuid(cls, user_uuid):
        return cls.query.filter_by(user_uuid=user_uuid).first()

    @classmethod
    def get_all_messages(cls):
        return Message.query.join(Conversation).all()


    @classmethod
    def does_exist(cls, trainer_uuid, user_uuid):
        from backend.models.trainer import Trainer
        trainer_conversation = Conversation.get_by_trainer_uuid(trainer_uuid)
        user_conversation = Conversation.get_user_by_user_uuid(user_uuid)
        if trainer_conversation.id is user_conversation.id:
            return trainer_conversation
        else:
            return False
