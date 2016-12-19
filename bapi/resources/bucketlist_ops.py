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

            try:
                limit = int(request.args.get('limit', '20'))
            except Exception:
                return {'message': 'Invalid limit value provided.'}

            try:
                page = int(request.args.get('page', '1'))
            except Exception:
                return {'message': 'Invalid page value provided.'}

            all_bucketlists = Bucketlist.query.filter(
                Bucketlist.created_by == g.user.id, Bucketlist.name.ilike(
                    '%' + q + '%')).paginate(page, limit, True)

            if all_bucketlists:

                all_pages = all_bucketlists.pages
                next_page = all_bucketlists.has_next
                prev_page = all_bucketlists.has_prev
                #
                # if next_page:
                #     next_page = str(request.url.root) + '/bucketlists?' + \
                #         'limit=' + str(limit) + '&page=' + str(page + 1)
                #
                # next_page = None
                #
                # if prev_page:
                #     prev_page = str(request.url.root) + '/bucketlists?' + \
                #         'limit=' + str(limit) + '&page=' + str(page - 1)
                # prev_page = None

                all_bucketlists = all_bucketlists.items

                return {'bucketlists': marshal(all_bucketlists, bucketlist_serial),
                        'total_pages': all_pages,
                        'next_page': next_page,
                        'prev_page': prev_page}

            return {'message': 'There are currently no existing bucketlists.'}, 200

        except Exception as e:
            return {'message': e}, 403

    @token_auth.login_required
    def post(self):
        try:

            existing = [item.name for item in Bucketlist.query.all()]

            self.bucketlist = reqparse.RequestParser()
            self.bucketlist.add_argument('name', type=str, required=True,
                                         location='json')
            self.args = self.bucketlist.parse_args()

            if self.args.name is " ":
                return {'message': 'Provide a name for the new bucketlist.'}, 400
            elif self.args.name in existing:
                return {'message': 'You already have a Bucketlist with that name.'}, 409

            new_bucketlist = Bucketlist(name=self.args.name, created_by=g.user.id)

            try:
                db.session.add(new_bucketlist)
                db.session.commit()
                return {'message': 'New Bucketlist created successfully.'}, 201
            except Exception:
                db.session.rollback()
                return {'message': 'An error occured during saving.'}, 500

        except AttributeError:
            return {'message': 'You are not authorized to access this URL.'}, 403


class SingleBucketlist(Resource):

    """List, update and delete a single Bucketlist."""

    @token_auth.login_required
    def get(self, id):
        try:

            requested_bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()

            if requested_bucketlist:
                return marshal(requested_bucketlist, bucketlist_serial)
            return {'message': 'You do not have a bucketlist with that id.'}, 404

        except AttributeError:
            return {'message': 'You are not authorized to access this URL.'}, 403

    @token_auth.login_required
    def put(self, id):
        try:

            existing = [item.name for item in Bucketlist.query.all()]

            self.new = reqparse.RequestParser()
            self.new.add_argument('name', type=str, required=True, location='json')
            self.args = self.new.parse_args()

            if self.args:
                bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()

                if bucketlist:

                    if self.args.name in existing:
                        return {'message': 'You already have a Bucketlist with that name.'}, 409

                    try:
                        bucketlist.name = self.args.name
                        db.session.commit()
                        return {'message': 'Bucketlist edited successfully.'}, 200
                    except Exception:
                        db.session.rollback()
                        return {'message': 'An error occured during saving.'}, 500

                return {'message': 'A bucketlist with that id was not found.'}, 404

            return {'message': 'Provide a new name to edit this Bucketlist.'}, 400

        except AttributeError:
            return {'message': 'You are not authorized to access this URL.'}, 403

    @token_auth.login_required
    def delete(self, id):
        try:

            if id:

                try:
                    Bucketlist.query.filter_by(created_by=g.user.id, id=id).delete()
                    BucketListItem.query.filter_by(bucketlist_id=id).delete()
                    db.session.commit()
                    return {'message': 'Bucketlist deleted successfully.'}, 200
                except Exception:
                    db.session.rollback()
                    return {'message': 'An error occured during saving.'}, 500

            return 'You must provide a bucketlist id to delete a Bucketlist.', 204

        except AttributeError:
            return {'message': 'You are not authorized to access this URL.'}, 403
