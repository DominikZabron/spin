import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin

from spin import app

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    username = Column(String(80), unique=True)
    password = Column(String(255))
    eur_account = relationship(
        "EurAccount", uselist=False, back_populates="user")
    bns_account = relationship(
        "BnsAccount", uselist=False, back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)
        self.eur_account = EurAccount()
        self.bns_account = BnsAccount()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class WalletMixin(object):
    id = Column(Integer, primary_key=True)
    balance = Column(DECIMAL(12, 2), default=0)

    @declared_attr
    def user_id(cls):
        return Column(UUIDType, ForeignKey('user.id'))


class EurAccount(db.Model, WalletMixin):
    __tablename__ = 'eur_account'
    user = relationship("User", back_populates="eur_account")


class BnsAccount(db.Model, WalletMixin):
    __tablename__ = 'bns_account'
    user = relationship("User", back_populates="bns_account")

