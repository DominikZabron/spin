import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin

from spin import app
from settings import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    username = Column(String(80), unique=True)
    password = Column(String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)
