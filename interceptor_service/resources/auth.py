from flask import Response, request
from flask_jwt_extended import create_access_token
from ..db.models import User
from flask_restful import Resource
import datetime
from functools import wraps


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.save()
        id = user.apikey
        return {'id': str(id)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(apikey=body.get('apikey'))
        if not user:
            return {'error': 'apikey invalid'}, 401

        expires = datetime.timedelta(days=360)
        access_token = create_access_token(identity=str(user.id),
                                           expires_delta=expires)
        return {'token': access_token}, 200
