from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
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
socket = SocketIO(app, cors_allowed_origins="")

from backend.models.revokedtoken import RevokedToken

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    print(decrypted_token)
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    print('tables created')
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
