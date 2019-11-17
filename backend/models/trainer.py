
from backend.helpers.serialization import to_json_trainer

from backend.models.conversation import Conversation
from backend import bcrypt
from backend import db

trainer_certification_association = db.Table('association_certification',
                                             db.Column('trainer_id', db.Integer,
                                                       db.ForeignKey('certification.certification_id')),
                                             db.Column('certification_id', db.Integer,
                                                       db.ForeignKey('trainer.trainer_id')))

trainer_conversation_association = db.Table('trainer_association_conversation',
                                            db.Column('trainer_id', db.Integer,
                                                      db.ForeignKey('conversation.conversation_id')),
                                            db.Column('conversation_id', db.Integer,
                                                      db.ForeignKey('trainer.trainer_id')))


class Trainer(db.Model):
    trainer_id = db.Column(db.Integer, primary_key=True)
    trainer_uuid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    biography = db.Column(db.Text)
    password = db.Column(db.Binary(60), nullable=False)
    rating = db.Column(db.Integer, default=0)
    certifications = db.relationship('Certification', secondary=trainer_certification_association,
                                     backref=db.backref('trainers', lazy='dynamic'))
    conversations = db.relationship("Conversation", secondary=trainer_conversation_association,
                                    backref=db.backref('trainers', lazy='dynamic'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(self):
        return {'trainers': list(map(lambda x: to_json_trainer(x), Trainer.query.all()))}

    @staticmethod
    def hash_password(password):
        print(password)
        return bcrypt.generate_password_hash(password=password)

    @staticmethod
    def verify_password(hash, attempted_password):
        return bcrypt.check_password_hash(hash, attempted_password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_uuid(cls, trainer_uuid):
        return cls.query.filter_by(trainer_uuid=trainer_uuid).first()

