from flask import g
from flask_restful import Resource, reqparse

from bapi import db
from bapi.bucketlist_models import Bucketlist, BucketListItem
from bapi.verification import token_auth


class CreateBucketlistItem(Resource):

    """Creates a new Item in Bucketlist."""

    @token_auth.login_required
    def post(self, id):
        try:
            create_item = reqparse.RequestParser()
            create_item.add_argument('name', type=str, required=True,
                                     location='json')
            create_item.add_argument('done', type=str, required=False,
                                     default='No', location='json')
            args = create_item.parse_args()

            bucketlist = Bucketlist.query.\
                filter_by(created_by=g.user.id, id=id).first()

            if not bucketlist:
                return {
                    'message': 'A bucketlist with that id does not exist.'
                    }, 404
            item_query = BucketListItem.query.filter_by(bucketlist_id=id).all()
            existing_items = [item.name for item in item_query]

            if not args.name.strip():
                return {
                    'message': 'Please provide a name for the new bucketlist\
                     item.'
                }, 400
            elif args.name in existing_items:
                return {'message': 'Item with that name already exists \
                    in this bucketlist.'}, 409
            elif args.done.lower() in ['no', 'yes']:
                done = args.done
            else:
                return {'message': "Use either 'Yes' or 'No' for done"}, 400

            new_bucketlist_item = BucketListItem(name=args.name, done=done)
            new_bucketlist_item.bucketlist_id = bucketlist.id
            db.session.add(new_bucketlist_item)
            db.session.commit()
            return {'message': "New item has been created."}, 201

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                    }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500


class BucketlistItems(Resource):

    """Update and Delete Bucketlist Items."""

    @token_auth.login_required
    def put(self, id, item_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=False,
                                location='json')
            parser.add_argument('done', type=str, required=False,
                                location='json')
            args = parser.parse_args()

            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id,
                                                    id=id).first()
            if not bucketlist:
                return {
                    'message': 'You do not have a bucketlist with that id.'
                    }, 404
            bucketlist_item = BucketListItem.query.filter_by(
                bucketlist_id=id, id=item_id).first()

            if not bucketlist_item:
                return {'message': 'An item with that id was not found.'}, 404
            item_query = BucketListItem.query.filter_by(bucketlist_id=id).all()
            existing_items = [item.name for item in item_query]

            if args.done is None:
                args.done = bucketlist_item.done
            elif args.done.lower() in ['yes', 'no']:
                bucketlist_item.done = args.done
            else:
                return {'message': "Use either 'Yes' or 'No' for done"}, 400

            if not args.name.strip():
                args.name = bucketlist_item.name
            elif args.name in existing_items:
                return {
                    'message': 'Item with that name exists in this bucketlist.'
                }, 409
            bucketlist_item.name = args.name
            db.session.commit()
            return {'message': 'Changes have been made succesfully.'}, 200

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                    }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500

    @token_auth.login_required
    def delete(self, id, item_id):
        try:
            bucketlist = \
                Bucketlist.query.filter_by(id=id, created_by=g.user.id).first()
            if not bucketlist:
                return {
                    'message': "You are not authorized to delete this item"
                    }, 401
            BucketListItem.query.filter_by(id=item_id).delete()
            db.session.commit()
            return {'message': 'Item has been deleted successfully.'}, 200

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                    }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500
