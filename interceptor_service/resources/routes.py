from .sale_order import SaleOrders, SaleOrder
from .auth import SignupApi, LoginApi
from .webhook import Webhook

def initialize_routes(api):
    api.add_resource(SaleOrders, '/api/saleorder/list')
    api.add_resource(SaleOrder, '/api/saleorder/<id>')
    api.add_resource(Webhook, '/api/webhook/saleorder')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')