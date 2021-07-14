from flask import Response, request
from ..db.models import Event, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from ..utilities.odoo_xmlrpc import query_get_data, query_create_data, query_write_data
import json


class Webhook(Resource):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        event =  Event(**body)
        event.save()
        return Response(json.dumps({"message":"success", "status": True}),status=200)