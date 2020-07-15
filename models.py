import datetime
from app import db
from uuid import uuid4


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.String(), primary_key=True, default=uuid4)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.datetime.now())


class Note(db.Model):
    __tablename__ = 'notes'
    uuid_author = db.Column(db.String(), db.ForeignKey('users.uuid'))
    id = db.Column(db.BigInteger(), primary_key=True)
    heading = db.Column(db.String())
    content = db.Column(db.Text())


class Todo(db.Model):
    __tablename__ = 'todos'
    uuid_author = db.Column(db.String(), db.ForeignKey('users.uuid'))
    id = db.Column(db.BigInteger(), primary_key=True)
    content = db.Column(db.Text())
    status = db.Column(db.Boolean(), default=False)


class Whitelist(db.Model):
    __tablename__ = 'whitelist'
    uuid_user = db.Column(db.String(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.now())
    token = db.Column(db.String(), unique=True)


class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    uuid_user = db.Column(db.String(), primary_key=True, unique=True)
    token = db.Column(db.String(), unique=True)
