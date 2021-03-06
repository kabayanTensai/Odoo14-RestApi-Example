from flask import Response, request
from ..db.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from ..utilities.odoo_xmlrpc import query_get_data, query_create_data, query_write_data
import json
from ..config import ODOO_API_KEY, ODOO_API_ENDPOINT
import requests as apiRequest



class SaleOrders(Resource):

    @jwt_required()
    def get(self):
        my_headers = {'Authorization': f"Bearer {ODOO_API_KEY}"}
        response = apiRequest.get(f"{ODOO_API_ENDPOINT}/list",headers=my_headers)
        if response.status_code == 200:
            resp_json = json.dumps(response.json())
            return Response(resp_json, mimetype="application/json", status=200)
        else:
            resp_json = json.dumps({"messsage":response.text})
            return Response(resp_json, mimetype="application/json", status=response.status_code)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        my_headers = {'Authorization': f"Bearer {ODOO_API_KEY}"}
        response = apiRequest.get(f"{ODOO_API_ENDPOINT}/",headers=my_headers,data=json.dumps(body))

        if response.status_code == 200:
            resp_json = json.dumps(response.json())
            return Response(resp_json, mimetype="application/json", status=200)
        else:
            resp_json = json.dumps({"messsage":response.text})
            return Response(resp_json, mimetype="application/json", status=response.status_code)
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        my_headers = {'Authorization': f"Bearer {ODOO_API_KEY}"}
        response = apiRequest.get(f"{ODOO_API_ENDPOINT}/update",headers=my_headers,data=json.dumps(body))
        
        if response.status_code == 200:
            resp_json = json.dumps(response.json())
            return Response(resp_json, mimetype="application/json", status=200)
        else:
            resp_json = json.dumps({"messsage":response.text})
            return Response(resp_json, mimetype="application/json", status=response.status_code)

class SaleOrder(Resource):
    @jwt_required()
    def get(self, id):
        my_headers = {'Authorization': f"Bearer {ODOO_API_KEY}"}
        response = apiRequest.get(f"{ODOO_API_ENDPOINT}/get/{id}",headers=my_headers)
        if response.status_code == 200:
            resp_json = json.dumps(response.json())
            return Response(resp_json, mimetype="application/json", status=200)
        else:
            resp_json = json.dumps({"messsage":response.text})
            return Response(resp_json, mimetype="application/json", status=response.status_code)
class SaleOrderDelete(Resource):   
    @jwt_required()
    def delete(self, id):
        my_headers = {'Authorization': f"Bearer {ODOO_API_KEY}"}
        response = apiRequest.get(f"{ODOO_API_ENDPOINT}/delete/{id}",headers=my_headers)
        if response.status_code == 200:
            resp_json = json.dumps(response.json())
            return Response(resp_json, mimetype="application/json", status=200)
        else:
            resp_json = json.dumps({"messsage":response.text})
            return Response(resp_json, mimetype="application/json", status=response.status_code)