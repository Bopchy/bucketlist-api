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

            if bucketlist:

                item_query = \
                    BucketListItem.query.filter_by(bucketlist_id=id).all()
                existing_items = [item.name for item in item_query]

                if args.done.lower() == 'no' or args.done.lower() == 'yes':
                    done = args.done
                else:
                    return {
                        'message': "Use either 'Yes' or 'No' for done"
                    }, 400

                if args.name == "" or args.name == " ":
                    return {
                        'message': 'Please provide a name for the new bucketlist\
                         item.'
                    }, 400
                elif args.name in existing_items:
                    return {'message': 'Item with that name already exists \
                        in this bucketlist.'}, 409
                new_bucketlist_item = BucketListItem(name=args.name,
                                                     done=done)
                new_bucketlist_item.bucketlist_id = bucketlist.id

                try:
                    db.session.add(new_bucketlist_item)
                    db.session.commit()
                    return {'message': "New item has been created."}, 201
                except Exception:
                    db.session.rollback()
                    return {'message': 'An error occured during saving.'},\
                        500

            return {'message': 'A bucketlist with that id does not \
                exist.'}, 404

        except AttributeError:
            return {'message': 'You are not authorized to access this item.'},\
                403


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
            if bucketlist:

                bucketlist_item = BucketListItem.query.filter_by(
                    bucketlist_id=id, id=item_id).first()

                if bucketlist_item:
                    item_query = BucketListItem.query.\
                        filter_by(bucketlist_id=id).all()
                    existing_items = [item.name for item in item_query]

                    if args.done is None:
                        args.done = bucketlist_item.done
                    elif args.done.lower() == 'no' or args.done.lower() == 'yes':
                        bucketlist_item.done = args.done
                    else:
                        return {
                            'message': "Use either 'Yes' or 'No' for done"
                        }, 400

                    if args.name is None:
                        args.name = bucketlist_item.name
                    elif args.name in existing_items:
                        return {
                            'message': 'Item with that name already exists in this bucketlist.'
                        }, 409
                    elif args.name is "" or args.name is " ":
                        return {
                            'message': 'You cannot have a nameless bucketlist item'
                        }, 400

                    bucketlist_item.name = args.name

                    try:
                        db.session.commit()
                        return {
                            'message': 'Changes have been made succesfully.'
                        }, 200
                    except Exception:
                        db.session.rollback()
                        return {
                            'message': 'An error occured during saving.'
                        }, 500

                return {'message': 'An item with that id was not found.'}, 404

            return {
                'message': 'You do not have a bucketlist with that id.'
            }, 404

        except AttributeError:
            return {
                'message': 'You are not authorized to access this item.'
            }, 403

    @token_auth.login_required
    def delete(self, id, item_id):
        try:

            bucketlist = \
                Bucketlist.query.filter_by(id=id, created_by=g.user.id).first()
            if bucketlist:

                try:
                    BucketListItem.query.filter_by(id=item_id).delete()
                    db.session.commit()
                    return {'message': 'Item has been deleted successfully.'},\
                        200
                except Exception:
                    db.session.rollback()
                    return {'message': 'An error occured during saving.'},\
                        200

            return {'message': "You are not authorized to delete this item"},\
                401

        except AttributeError:
            return {'message': 'You are not authorized to access this item.'},\
                403
