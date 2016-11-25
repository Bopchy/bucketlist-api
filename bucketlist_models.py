from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import Config


bucketlist.config.from_object('config')
db = SQLAlchemy(bucketlist)


class Users(db.Model):

    """docstring for Users"""

    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(Password)
    email = Column(String, nullable=False, unique=True)


class Bucketlist(db.Model):

    """docstring for Bucketlists"""

    __tablename__ = 'bucketlist'
    _id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    item =
    date_created = Column()
    date_modified = Column()

engine = create_engine('mysql://bopchy:@localhost/bucketlist_db')
connection = engine.connect()
