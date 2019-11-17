from backend import db
import datetime


class Message(db.Model):
    message_id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(400), unique=False, nullable=False)
    sender_id = db.Column(db.String(120), unique=False, nullable=False)
    receiver_id =  db.Column(db.String(120), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.conversation_id'))
    #attachments

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def convert_to_datatime(time):
        return datetime.datetime.fromtimestamp(time/1000.0)