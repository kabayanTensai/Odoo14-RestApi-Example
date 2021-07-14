# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request, Response
from werkzeug.exceptions import BadRequest, Unauthorized
import json
import requests as apiRequest


class efishery_module(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        print(">>>>>>>>>>>>", self, vals)
        
        self._send_event_webhook(vals,'created')
        return super().create(vals)

    def write(self, vals):
        print(">>>>>>>>>>>> write", self, vals)
        
        self._send_event_webhook(vals,'updated')

        return super().write(vals)

    def unlink(self):
        print(">>>>>>>>>>>> Delete", self.id)
        self._send_event_webhook({"sale_order":self.id},'deleted')
        return super().unlink()

    def _get_token_webhook(self):
        apikey = self.env['ir.config_parameter'].get_param(
            'efishery_module.apikey')
        headers = {'Content-Type': 'application/json'}
        webhook_url = self.env['ir.config_parameter'].get_param(
            'efishery_module.webhook_url')
        response = apiRequest.post(f"{webhook_url}/api/auth/login",
                                   data=json.dumps({"apikey": apikey}), headers=headers)
        json_response = response.json()
        return  json_response['token']

    def _send_event_webhook(self, vals, event):
        payload = vals.copy()
        payload['order_id']=self.id
        token = self._get_token_webhook()
        webhook_url = self.env['ir.config_parameter'].get_param(
            'efishery_module.webhook_url')
        my_headers = {'Authorization': f"Bearer {token}",
                      'Content-Type': 'application/json'}

        data = json.dumps(
            {"event": f"service.sales_order.{event}", "payload": payload})
        webhook_resp = apiRequest.post(
            f"{webhook_url}/api/webhook/saleorder", headers=my_headers, data=data)


class efishery_module_settings(models.TransientModel):
    _inherit = "res.config.settings"

    webhook_url = fields.Char(string='Webhook URL',
                              config_parameter="efishery_module.webhook_url")
    apikey = fields.Char(
        string="Api Key", config_parameter="efishery_module.apikey")
    token = fields.Char(
        string="Token",  config_parameter="efishery_module.token")

    @api.model
    def get_values(self):
        res = super(efishery_module_settings, self).get_values()
        res.update(
            webhook_url=self.env['ir.config_parameter'].sudo(
            ).get_param('efishery_module.webhook_url'),
            apikey=self.env['ir.config_parameter'].sudo(
            ).get_param('efishery_module.apikey'),
            token=self.env['ir.config_parameter'].sudo(
            ).get_param('efishery_module.token'),
        )
        return res

    def set_values(self):
        super(efishery_module_settings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        field1 = self.webhook_url or ''
        field2 = self.apikey or ''
        field3 = self.token or ''

        param.set_param('efishery_module.webhook_url', field1)
        param.set_param('efishery_module.apikey', field2)
        param.set_param('efishery_module.token', field3)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_my_api_key(cls):
        api_key = request.httprequest.headers.get("Authorization")
        split_api_key = api_key.split(' ')
        api_key = split_api_key[1]
        if not api_key:

            raise Unauthorized(response=Response(json.dumps({
                "success": False,
                "message": "Token Not Found"
            }), 401))

        user_id = request.env["res.users.apikeys"]._check_credentials(
            scope="rpc", key=api_key
        )
        if not user_id:
            raise BadRequest("API key invalid")

        request.uid = user_id
