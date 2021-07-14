from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import secrets

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    apikey = db.StringField(unique=True,default=secrets.token_hex(16))

class Event(db.Document):
    event = db.StringField(required=True)
    payload = db.DictField(required=True)


