from resources import BapiLogin, BapiRegister, Bucketlists, SingleBucketlist, CreateBucketlistItem, BucketlistItems


def routes(api):
    # API resource routing setup
	api.add_resource(BapiLogin, '/auth/login', endpoint='bapilogin')
	api.add_resource(BapiRegister, '/auth/register', endpoint='register')
	api.add_resource(Bucketlists, '/bucketlists/', endpoint='bucketlists')
	api.add_resource(SingleBucketlist, '/bucketlists/<id>', endpoint='singlebucketlist')
	api.add_resource(CreateBucketlistItem, '/bucketlists/<id>/items/', endpoint='createbucketlistitem')
	api.add_resource(BucketlistItems, '/bucketlists/<id>/items/<item_id>', endpoint='bucketlistitems')
