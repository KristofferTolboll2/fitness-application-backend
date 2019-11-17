from backend import db
from backend.helpers.serialization import to_json_trainer
from backend import bcrypt

user_conversation_association = db.Table('user_association_conversation',
                                         db.Column('user_id', db.Integer,
                                                   db.ForeignKey('conversation.conversation_id')),
                                         db.Column('conversation_id', db.Integer,
                                                   db.ForeignKey('user.user_id')))


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    biography = db.Column(db.Text)
    password = db.Column(db.Binary(60), nullable=False)
    rating = db.Column(db.Integer, default=0)
    conversations = db.relationship("Conversation", secondary=user_conversation_association,
                                    backref=db.backref('users', lazy='dynamic'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(self):
        return {'users': list(map(lambda x: to_json_trainer(x), User.query.all()))}

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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
