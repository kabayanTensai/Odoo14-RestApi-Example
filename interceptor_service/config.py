from os import environ


_ = environ.get

JWT_SECRET_KEY = _('JWT_SECRET_KEY','t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')
FLASK_PORT = _('FLASK_PORT', 5000)
ODOO_API_KEY = _('ODOO_API_KEY','1d91aaf49762c48030ef0259581b33ead88eb3f8')
ODOO_API_ENDPOINT = _('ODOO_API_ENDPOINT','https://tensai13coder.tech/order')
MONGODB_HOST = _('MONGODB_HOST','mongodb://localhost:27017/efishery-interceptor')