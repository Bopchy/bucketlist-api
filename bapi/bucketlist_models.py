from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bapi import db, bcrypt
from config import Config


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
        self.hashed_password = bcrypt.generate_password_hash(hashed_password)

    def check_password(self, hashed_password):
        print('user %s db %s' % (hashed_password, self.hashed_password))
        return bcrypt.check_password_hash(self.hashed_password, hashed_password)

    def generate_auth_token(self, expiration=6000):
        # Creates an encoded string from dictionary containing the user's
        # username as token, with an expiration of 10 minutes.
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'username': self.username, 'id': self.id}).decode('utf-8')


class Bucketlist(db.Model):

    """Model for Bucketlist table"""

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True)
    item = db.relationship('BucketListItem', backref='bucketlistitem',
                           cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(),
                              onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


class BucketListItem(db.Model):

    """Model for BucketlistListItem table"""

    __tablename__ = 'bucketlistitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(),
                              onupdate=db.func.now())
    done = db.Column(db.String(3), default='No')

    def __init__(self, name, done):
        self.name = name
        self.done = done
