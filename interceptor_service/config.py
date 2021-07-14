from os import environ


_ = environ.get

JWT_SECRET_KEY = _('JWT_SECRET_KEY','t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')
FLASK_PORT = _('FLASK_PORT', 5000)
ODOO_API_KEY = _('ODOO_API_KEY','933d781224995611faa0b943632c50b22c322e66')
ODOO_API_ENDPOINT = _('ODOO_API_ENDPOINT','http://localhost:8069/order')
MONGODB_HOST = _('MONGODB_HOST','mongodb://root:pass@localhost:27017/efishery-interceptor')