from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .db.db import initialize_db
from flask_restful import Api
from .resources.routes import initialize_routes
from . import config

app = Flask(__name__)
app.config.from_object(config)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': config.MONGODB_HOST
}

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=config.FLASK_PORT)
