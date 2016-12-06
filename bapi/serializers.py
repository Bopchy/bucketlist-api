from flask_restful import fields


bucketlist_item_serial = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
}

bucketlist_serial = {
    'id': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(bucketlist_item_serial),
    'date_created': fields.DateTime, 
    'date_modified': fields.DateTime,
    'created_by': fields.String
}

bapi_users = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}
