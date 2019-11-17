import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_claims
from flask_cors import CORS
from flask_socketio import SocketIO, emit

POSTGRES = {
    'user': 'kristoffer',
    'pw': 'toor123',
    'db': 'fitness_application',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the_secret_sauce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'dodo123hvadsaaderbruhbruh'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000')

from backend.helpers.type_helper import is_trainer
from backend.models.revokedtoken import RevokedToken
from backend.models.conversation import Conversation
from backend.models.message import Message


@socketio.on('test')
def test(data):
    print("test")
    print(data)
    emit("response", {'data': 'test'})

from backend.helpers.type_helper import does_conversation_exist, get_existing_conversation
@jwt_required
@socketio.on('send_message_user_to_trainer')
def on_send_message_user_to_trainer(data):
    print("Message received")
    user_uuid = data['sender'] #should be swtiched
    trainer_uuid = data['receiver']
    content = data['content']
    print(data)
    print(user_uuid, trainer_uuid)
    if does_conversation_exist(user_uuid, trainer_uuid):
        print("does exists")
        conversation = get_existing_conversation(user_uuid, trainer_uuid)
        new_message = Message(sender_id=user_uuid, receiver_id=trainer_uuid, content=content, conversation_id=conversation.conversation_id)
        conversation.messages.append(new_message)
        db.session.commit()
        print(conversation.get_all_messages())
        return json.dumps({'message': 'Successfully added message', 'status': 'success'})
    else:
        print("does not exists")
        conversation = Conversation(trainer_uuid=trainer_uuid, user_uuid=user_uuid)
        conversation.save_to_db()
        print(conversation)




@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    print(decrypted_token)
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    print('tables created')
    result = db.engine.execute("DROP TABLE if exists certification cascade ")
    result1 = db.engine.execute("DROP TABLE if exists trainer cascade ")
    result = db.engine.execute("DROP TABLE if exists conversation cascade ")
    result1 = db.engine.execute("DROP TABLE if exists message cascade ")
    print(result)
    print(result1)
    db.drop_all()
    db.create_all()




from backend.resources.resources import TrainerRegistration, TrainerLogin, TokenRefresh, UserLogoutRefresh, \
    UserLogoutAccess, AllUsers, UserLogin, AllTrainers, SecretResource, VerifyAndGetTrainer, TrainerById

from backend.models.trainer import Trainer

api.add_resource(TrainerRegistration, '/api/trainer/register')
api.add_resource(TrainerLogin, '/api/trainer/login')
api.add_resource(UserLogoutAccess, '/api/logout/access')
api.add_resource(UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(TokenRefresh, '/api/token/refresh')
api.add_resource(AllTrainers, '/api/trainer/all')
api.add_resource(SecretResource, '/api/secret')
api.add_resource(VerifyAndGetTrainer, '/api/trainer/auth')
api.add_resource(TrainerById, '/api/trainer/profile')
