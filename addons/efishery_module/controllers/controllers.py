# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
from werkzeug.exceptions import BadRequest, InternalServerError
import json
from datetime import datetime


class EfisheryModule(http.Controller):
    @http.route('/order/list/', auth='my_api_key', method=['GET'])
    def index(self, **kw):
        try:
            headers = {'Content-Type': 'application/json'}
            sale_order_rec = request.env['sale.order'].sudo().search([])
            sale_order = []
            for rec in sale_order_rec:
                order_line = []
                for line in rec.order_line:
                    order_line.append({"id": line.id,
                                       "product_id": line.product_id.id,
                                       "product_uom_qty": line.product_uom_qty,
                                       "product_uom": line.product_uom.name,
                                       "price_unit": line.price_unit})
                date_order = rec.date_order
                rec_val = {
                    "id": rec.id,
                    "name": rec.name,
                    "partner_id": rec.partner_id.id,
                    "date_order": date_order.strftime("%m/%d/%Y, %H:%M:%S"),
                    "company_id": rec.company_id.id,
                    "order_line": order_line
                }
                sale_order.append(rec_val)

            data = json.dumps(sale_order)
            return Response(data, headers=headers)
        except:
            return Response(json.dumps({
                "success": False,
                "message": "Internal Server Error"
            }), 500)

    @http.route('/order/get/<int:rec_id>', auth='my_api_key', method=['GET'])
    def get_sale_order_by_id(self, rec_id, **params):
        try:
            headers = {'Content-Type': 'application/json'}
            sale_order = request.env['sale.order'].sudo().search(
                [['id', '=', rec_id]])
            if len(sale_order) == 0:
                return Response(json.dumps({
                "success": False,
                "message": "id not found"
            }), status=400)

            order_line = []
            product = []
            uom = [{"id": sale_order.order_line[0].product_uom.id,
                    "name":sale_order.order_line[0].product_uom.name,
                    "description":sale_order.order_line[0].product_uom.uom_type}]
            for line in sale_order.order_line:
                order_line.append({"id": line.id,
                                   "product_id": line.product_id.id,
                                   "product_uom_qty": line.product_uom_qty,
                                   "product_uom": line.product_uom.name,
                                   "price_unit": line.price_unit})
                product.append({"id": line.product_id.id,
                                "name": line.product_id.name,
                                "description": line.product_id.description_sale,
                                "price": line.product_id.list_price})

            partner = [{"partner_id": sale_order.partner_id.id,
                        "name": sale_order.partner_id.name,
                        "address": f"{sale_order.partner_id.street} {sale_order.partner_id.street2}, {sale_order.partner_id.city},{sale_order.partner_id.state_id.name},{sale_order.partner_id.zip},{sale_order.partner_id.country_id.name}"
                        }
                       ]
            company = [{"id": sale_order.company_id.id,
                        "name": sale_order.company_id.name,
                        "description": sale_order.company_id.website}]
            date_order = sale_order.date_order
            data_sale_order = {
                "name": sale_order.name,
                "partner_id": sale_order.partner_id.id,
                "date_order": date_order.strftime("%m/%d/%Y, %H:%M:%S"),
                "company_id": sale_order.company_id.id,
                "relationship": {"partner": partner, "product": product, "company": company, "uom": uom},
                "order_line": order_line
            }
            return Response(json.dumps(data_sale_order), headers=headers)
        except:
            return Response(json.dumps({
                "success": False,
                "message": "Internal Server Error"
            }), 500)

    @http.route('/order', auth='my_api_key', method=['POST'], csrf=False)
    def create_sale_order(self, **params):
        error_detail = {}
        try:
            headers = {'Content-Type': 'application/json'}
            data = json.loads(request.httprequest.data)

            name = data.get('name')
            if name is None:
                error_detail['name'] = "Required"
            partner_id = data.get('partner_id')
            if partner_id is None:
                error_detail['partner_id'] = 'Not Found'

            date_order = data.get('date_order')
            if date_order is None:
                error_detail['date_order'] = "Invalid Format Date"
            company_id = data.get('company_id')
            if company_id is None:
                error_detail['company_id'] = "Required"
            dupe_check = request.env['sale.order'].sudo().search(
                [['name', '=', name]])

            if len(dupe_check) != 0:
                return Response(json.dumps({
                    "success": False,
                    "data": {
                        "name": "Already exists"
                    }
                }), 409)

            with http.request.env.cr.savepoint():
                order_line = [(0, '_', {"product_id": int(order['product_id']),
                                        "product_uom_qty":int(order['product_uom_qty']),
                                        "price_unit":int(order['price_unit'])})
                              for order in data['order_line']]
                order = request.env['sale.order'].sudo().create({"name": name,
                                                                 "partner_id": partner_id,
                                                                 "date_order": date_order,
                                                                 "company_id": company_id,
                                                                 "order_line":order_line})
                return Response(json.dumps({"success": True, "message": "Success"}), headers=headers)
        except Exception as e:
            return Response(json.dumps({
                "success": False,
                "data": error_detail,
                "error_message": f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            }), 500)

    @http.route('/order/update', auth='my_api_key', method=['PUT'], csrf=False)
    def update_sale_order(self, **params):
        try:
            headers = {'Content-Type': 'application/json'}
            data = json.loads(request.httprequest.data)
            name = data['name']

            partner_id = data['partner_id']
            date_order = data['date_order']
            company_id = data['company_id']
            sale_order_id = data['id']

            sale_order = request.env['sale.order'].sudo().search(
                [['id', '=', 'sale_order_id']])
            if len(sale_order) == 0:
                return Response("order id not found", status=400)

            order_line = [(1, order['id'], {"product_id": order['product_id'],
                                            "product_uom_qty":order['product_uom_qty'],
                                            "price_unit":order['price_unit']})
                        for order in data['order_line']]

            sale_order.sudo().write({"partner_id": partner_id,
                                    "date_order": date_order,
                                    "company_id": company_id,
                                    "order_line": order_line})

            return Response(json.dumps({"success": True, "message": "Success"}), headers=headers)
        except Exception as e:
            return Response(json.dumps({
                "success": False,
                "error_message": f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            }), 400)


#     @http.route('/efishery_module/efishery_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('efishery_module.listing', {
#             'root': '/efishery_module/efishery_module',
#             'objects': http.request.env['efishery_module.efishery_module'].search([]),
#         })

#     @http.route('/efishery_module/efishery_module/objects/<model("efishery_module.efishery_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('efishery_module.object', {
#             'object': obj
#         })
