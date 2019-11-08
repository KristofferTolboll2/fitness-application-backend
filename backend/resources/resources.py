from flask_restful import Resource, reqparse, inputs
from backend.models.trainer import Trainer
from backend.models.trainer import Certification
from backend.models.revokedtoken import RevokedToken
from backend import bcrypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims)
from backend.helpers.serialization import to_json_trainer
import uuid
trainer_registration_parser = reqparse.RequestParser()
trainer_registration_parser.add_argument('email',
                                         type=inputs.regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
                                         help="Field Email can't be blank or invalid", required=True)
trainer_registration_parser.add_argument('password', help="Field Password can't be blank", required=True)
trainer_registration_parser.add_argument('first_name', help="Field Password can't be blank", required=True)
trainer_registration_parser.add_argument('last_name', help="Field Password can't be blank", required=True)
trainer_registration_parser.add_argument('certifications', help="The certifications for the trainer", action="append")

trainer_login_parser = reqparse.RequestParser()
trainer_login_parser.add_argument('email', type=str, help='must enter username')
trainer_login_parser.add_argument('password', type=str, help='must enter password')


trainer_update_parser = reqparse.RequestParser()
trainer_update_parser.add_argument('email',
                                         type=inputs.regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
                                         help="Field Email can't be blank or invalid", required=False)
trainer_update_parser.add_argument('password', help="Field Password can't be blank", required=False)
trainer_update_parser.add_argument('first_name', help="Field Password can't be blank", required=False)
trainer_update_parser.add_argument('last_name', help="Field Password can't be blank", required=False)
trainer_update_parser.add_argument('certifications', help="Ceritifications")

trainer_by_id_parser = reqparse.RequestParser()
trainer_by_id_parser.add_argument('id', type=str, help="ID on the trainer you want to fetch", required=True)


class VerifyAndGetTrainer(Resource):
    @jwt_required
    def get(self):
        trainer_email = get_jwt_identity()
        print(trainer_email)
        new_trainer = Trainer.find_by_email(trainer_email)
        if not new_trainer:
            return {'err': 'Authentication failed'}, 401
        else:
            return {'data': to_json_trainer(new_trainer)}, 200



class TrainerRegistration(Resource):
    def post(self):
        data = trainer_registration_parser.parse_args()
        # profile_picture = request.files['profile_picture']
        hashed_password = Trainer.hash_password(data['password'])
        trainer_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))
        certifications = data['certifications']
        trainer_certifications = []
        if certifications:
            for certification in certifications:
                attempted_certification = Certification.find_by_name(certification)
                print(attempted_certification)
                if attempted_certification:
                    trainer_certifications.append(attempted_certification)
                else:
                    new_certification = Certification(name=certification, description="", score=0)
                    new_certification.save_to_db()
                    print(new_certification)
                    trainer_certifications.append(new_certification)
        print(trainer_certifications[0].name)
        new_trainer = Trainer(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            uuid=trainer_uuid,
            certifications=trainer_certifications
        )
        try:
            new_trainer.save_to_db()
            access_token = create_access_token(identity=trainer_uuid)
            refresh_token = create_refresh_token(identity=trainer_uuid)
            return {'msg':
                    f'Trainer with name {new_trainer.first_name} {new_trainer.last_name} created',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        except Exception as e:
            print(e)  # should be logged
            return {'err': 'Something went wrong'}, 401


class TrainerById(Resource):
    @jwt_required
    def get(self):
        data = trainer_by_id_parser.parse_args()
        trainer_uuid = data['id']
        new_trainer = Trainer.find_by_uuid(trainer_uuid)
        if not new_trainer:
            return {'msg': f"Trainer with uuid {trainer_uuid} not found"}, 401
        else:
            return {'msg': to_json_trainer(new_trainer)}

class TrainerLogin(Resource):
    def post(self):
        data = trainer_login_parser.parse_args()
        current_trainer = Trainer.find_by_email(data['email'])
        if not current_trainer:
            return {'msg': f'Trainer {current_trainer} not found'}, 401

        if bcrypt.check_password_hash(current_trainer.password, data['password']):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {'message':
                    f'Trainer Logged in with email {current_trainer.email}',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'id': current_trainer.trainer_id,
                    'traner': to_json_trainer(current_trainer)
                    }
        else:
            # create log for wrong credentials
            return {'msg': 'wrong credentials'}, 401


class AllTrainers(Resource):
    @jwt_required
    def get(self):
        return {'message': Trainer.return_all()}

class UpdateTrainer(Resource):
    @jwt_required
    def put(self):
        trainer_email = get_jwt_identity()
        new_trainer = Trainer.find_by_email(trainer_email)
        #certifications = data['certifications']


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # can also refrence trainer
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class GetTrainerById(Resource):
    pass


class UserLogin(Resource):
    def post(self):
        return {'message': 'User login'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jwt = get_raw_jwt()['jwt']
        try:
            revoked_token = RevokedToken(jwt_identitfier=jwt)
            revoked_token.add()
            return {'msg': 'Jwt was revoked successfully'}
        except Exception as e:
            # log here
            return {'err': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jwt = get_raw_jwt()['jwt']
        try:
            revoked_token = RevokedToken(jwt_identifier=jwt)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}




class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
