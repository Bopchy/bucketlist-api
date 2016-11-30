from bapi import db


DB = db

class Users(db.Model):

    """Model for Users table"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True,
                         nullable=False)
    hashed_password = db.Column(db.String(65))
    email = db.Column(db.String(65), nullable=False, unique=True)
    bucketlists = db.relationship('Bucketlist', backref='bucketlist',
                                  cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, username, hashed_password, email):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password


class Bucketlist(db.Model):

    """Model for Bucketlist table"""

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, index=True)
    item = db.relationship('BucketListItem', backref='bucketlistitem',
                           cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(),
                              onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name):
        self.name = name


class BucketListItem(db.Model):

    """Model for BucketlistListItem table"""

    __tablename__ = 'bucketlistitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(),
                              onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name
