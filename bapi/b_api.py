
from flask import request, url_for
from flask_restful import Api, marshal_with

from bapi import app
from config import config
from resources import * 



api = Api(app)
app.config.from_object(config['development'])


# API resource routing setup 
api.add_resource(BapiUsers, '/auth/login', endpoint='bapiusers')
api.add_resource(BapiRegister, '/auth/register', endpoint='register')
api.add_resource(Bucketlists, '/bucketlists/', endpoint='bucketlists')
api.add_resource(SingleBucketlist, '/bucketlists/<id>', endpoint='singlebucketlist')
api.add_resource(CreateBucketlistItem, '/bucketlists/<id>/items/', endpoint='createbucketlistitem')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/<item_id>', endpoint='bucketlistitems')



if (__name__) == '__main__':
    app.run(debug=True)
