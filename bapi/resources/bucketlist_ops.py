from urllib.parse import urlparse
from flask import g
from flask_restful import Resource, reqparse, request, marshal

from bapi import db
from bapi.verification import token_auth
from bapi.bucketlist_models import Bucketlist, BucketListItem
from bapi.serializers import bucketlist_serial


class Bucketlists(Resource):

    """Creates a new Bucketlist and lists all Bucketlists.

    @token_auth.login_required ensures that users are required
    to be authenticated and have a token."""

    @token_auth.login_required
    def get(self):
        try:
            q = request.args.get('q', '')
            limit = int(request.args.get('limit', '20'))
            page = int(request.args.get('page', '1'))

            all_bucketlists = Bucketlist.query.filter(
                Bucketlist.created_by == g.user.id, Bucketlist.name.ilike(
                    '%' + q + '%')).paginate(page, limit, True)

            if not all_bucketlists:
                return {'message': 'There are currently no existing bucketlists.\
                    '}, 200
            all_pages = all_bucketlists.pages
            next_page = all_bucketlists.has_next
            prev_page = all_bucketlists.has_prev
            url = urlparse(request.url)
            root_url = url.scheme + '://' + url.netloc + url.path

            if next_page:
                next_page = root_url + 'limit=' + str(limit) + '&page=' + \
                    str(page + 1)
            else:
                next_page = None

            if prev_page:
                prev_page = root_url + 'limit=' + str(limit) + '&page=' + \
                    str(page - 1)
            else:
                prev_page = None

            all_bucketlists = all_bucketlists.items

            return {'bucketlists': marshal(all_bucketlists, bucketlist_serial),
                    'total_pages': all_pages,
                    'next_page': next_page,
                    'prev_page': prev_page}

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                }, 403
            return {'message': 'Invalid value provided.'}

    @token_auth.login_required
    def post(self):
        try:
            existing = [item.name for item in Bucketlist.query.all()]

            self.bucketlist = reqparse.RequestParser()
            self.bucketlist.add_argument('name', type=str, required=True,
                                         location='json')
            self.args = self.bucketlist.parse_args()

            if not self.args.name.strip():
                return {'message': 'Provide a name for the new bucketlist.'}, \
                    400
            elif self.args.name in existing:
                return {
                    'message': 'You already have a Bucketlist with that name.'
                }, 409

            new_bucketlist = Bucketlist(name=self.args.name,
                                        created_by=g.user.id)
            db.session.add(new_bucketlist)
            db.session.commit()
            return {'message': 'New Bucketlist created successfully.'}, 201

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500


class SingleBucketlist(Resource):

    """List, update and delete a single Bucketlist."""

    @token_auth.login_required
    def get(self, id):
        try:
            requested_bucketlist = \
                Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()

            if not requested_bucketlist:
                return {
                    'message': 'You do not have a bucketlist with that id.'
                    }, 404
            return marshal(requested_bucketlist, bucketlist_serial)

        except AttributeError:
            return {
                'message': 'You are not authorized to access this item.'
                }, 403

    @token_auth.login_required
    def put(self, id):
        try:
            existing = [item.name for item in Bucketlist.query.all()]

            self.new = reqparse.RequestParser()
            self.new.add_argument('name', type=str, required=True,
                                  location='json')
            self.args = self.new.parse_args()

            if not self.args:
                return {
                    'message': 'Provide a new name to edit this Bucketlist.'
                }, 400
            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id,
                                                    id=id).first()

            if not bucketlist:
                return {
                    'message': 'A bucketlist with that id was not found.'
                }, 404
            if self.args.name in existing:
                return {
                    'message': 'You already have a Bucketlist with that name.'
                }, 409
            bucketlist.name = self.args.name
            db.session.commit()
            return {'message': 'Bucketlist edited successfully.'}, 200

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500

    @token_auth.login_required
    def delete(self, id):
        try:
            Bucketlist.query.filter_by(created_by=g.user.id,
                                       id=id).delete()
            BucketListItem.query.filter_by(bucketlist_id=id).delete()
            db.session.commit()
            return {'message': 'Bucketlist deleted successfully.'}, 200

        except Exception as e:
            if e is AttributeError:
                return {
                    'message': 'You are not authorized to access this item.'
                }, 403
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500
