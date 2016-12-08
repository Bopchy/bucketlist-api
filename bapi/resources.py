from flask import g
from flask_restful import Resource, reqparse, marshal, request

from bucketlist_models import DB, Users, Bucketlist, BucketListItem
from serializers import bucketlist_serial
from verification import token_auth


class Login(Resource):

    """Logs in users and returns token."""

    def post(self):
        self.user = reqparse.RequestParser()
        self.user.add_argument('username', type=str, required=True,
                               location='json')
        self.user.add_argument('password', type=str, required=True,
                               location='json')
        self.args = self.user.parse_args()

        user = Users.query.filter_by(username=self.args.username).first()

        try:
            if user:
                if user.check_password(self.args.password):
                    token = user.generate_auth_token()
                    return {'token': token}, 200
                return {'message': 'Invalid password'}, 401
            return {'message': 'That username does not exist.'}, 401
        except Exception:
            return {'message': 'There was an error logging you in.'}, 400


class Register(Resource):

    """Registers new users."""

    def post(self):
        self.bapi_users = reqparse.RequestParser()
        self.bapi_users.add_argument('username', type=str, required=True,
                                     location='json')
        self.bapi_users.add_argument('email', type=str, required=True,
                                     location='json')
        self.bapi_users.add_argument('password', type=str, required=True,
                                     location='json')
        self.args = self.bapi_users.parse_args()

        if '@' not in self.args.email or '.com' not in self.args.email:
            return {'message': 'Invalid email provided'}, 422
        user = Users.query.filter_by(username=self.args.username).first()
        if user:
            return {'message': 'A user with that name already exists.'}, 409
        user_email = Users.query.filter_by(email=self.args.email).first()
        if user_email:
            return {'message': 'That email is already in use.'}, 409
        user = Users(username=self.args.username, email=self.args.email,
                     hashed_password=self.args.password)

        try:
            DB.session.add(user)
            DB.session.commit()
            return {'message': 'New user has been added successfully.'}, 201
        except Exception:
            DB.session.rollback()
            return {'message': 'An error occured during saving.'}, 500


class Bucketlists(Resource):

    """Creates a new Bucketlist and lists all Bucketlists.

    @token_auth.login_required ensures that users are required
    to be authenticated and have a token."""

    @token_auth.login_required
    def get(self):
        # Lists all existing bucketlists
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
            Bucketlist.created_by == g.user.id).paginate(page, limit, True)

        if all_bucketlists:

            if q:
                search_results = Bucketlist.query.filter(Bucketlist.created_by == g.user.id.id, Bucketlist.name.ilike(
                    '%' + q + '%')).paginate(int(page), int(limit), True).items
                if not search_results:
                    return {'message': 'Found no bucketlists matching your query.'}, 200
                return marshal(search_results, bucketlist_serial)

            all_pages = all_bucketlists.pages
            next_page = all_bucketlists.has_next
            prev_page = all_bucketlists.has_prev

            if next_page:
                next_page = str(request.url.root) + '/bucketlists?' + \
                    'limit=' + str(limit) + '&page=' + str(page + 1)
            next_page = None

            if prev_page:
                prev_page = str(request.url.root) + '/bucketlists?' + \
                    'limit=' + str(limit) + '&page=' + str(page - 1)
            prev_page = None

            all_bucketlists = all_bucketlists.items

            return {'bucketlists': marshal(all_bucketlists, bucketlist_serial),
                    'total_pages': all_pages,
                    'next_page': next_page,
                    'prev_page': prev_page}

        return {'message': 'There are currently no existing bucketlists.'}, 200

    @token_auth.login_required
    def post(self):

        existing = [item.name for item in Bucketlist.query.all()]

        # Creates a new bucketlist
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
            DB.session.add(new_bucketlist)
            DB.session.commit()
            return {'message': 'New Bucketlist created successfully.'}, 201
        except Exception:
            DB.session.rollback()
            return {'message': 'An error occured during saving.'}, 500


class SingleBucketlist(Resource):

    """List, update and delete a single Bucketlist."""

    @token_auth.login_required
    def get(self, id):
        # Lists a single bucketlist
        requested_bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()

        if requested_bucketlist:
            return marshal(requested_bucketlist, bucketlist_serial)
        return {'message': 'You do not have a bucketlist with that id.'}, 404

    @token_auth.login_required
    def put(self, id):

        existing = [item.name for item in Bucketlist.query.all()]

        # Updates a single bucketlist
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
                    DB.session.commit()
                    return {'message': 'Bucketlist edited successfully.'}, 200
                except Exception:
                    DB.session.rollback()
                    return {'message': 'An error occured during saving.'}, 500

            return {'message': 'A bucketlist with that id was not found.'}, 404

        return {'message': 'Provide a new name to edit this Bucketlist.'}, 400

    @token_auth.login_required
    def delete(self, id):
        # Deletes a single bucketlist
        if id:

            try:
                Bucketlist.query.filter_by(created_by=g.user.id, id=id).delete()
                DB.session.commit()
                return {'message': 'Bucketlist deleted successfully.'}, 200
            except Exception:
                DB.session.rollback()
                return {'message': 'An error occured during saving.'}, 500

        return 'You must provide a bucketlist id to delete a Bucketlist.', 204


class CreateBucketlistItem(Resource):

    """Creates a new Item in Bucketlist."""

    @token_auth.login_required
    def post(self, id):

        existing_items = BucketListItem.query.filter_by(bucketlist_id=id)

        create_item = reqparse.RequestParser()
        create_item.add_argument('name', type=str, required=True,
                                 location='json')
        create_item.add_argument('done', type=str, required=False, default='No',
                                 location='json')
        args = create_item.parse_args()

        if id:

            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()
            if bucketlist:

                if args.done == 'No':
                    done = False
                elif args.done == 'Yes':
                    done = True
                else:
                    return {'message': "Use either 'Yes' or 'No' for done"}, 400

                if args.name in existing_items.name:
                    return {'message': 'Item with that name already exists in this bucketlist.'}, 409
                new_bucketlist_item = BucketListItem(name=args.name, done=done)
                new_bucketlist_item.bucketlist_id = bucketlist.id

                try:
                    DB.session.add(new_bucketlist_item)
                    DB.session.commit()
                    return {'message': " New item has been created."}, 201
                except Exception:
                    DB.session.rollback()
                    return {'message': 'An error occured during saving.'}, 500

            return {'message': 'A bucketlist with that id does not exist.'}, 404

        return {'message': 'Provide a bucketlist id for this operation.'}, 400


class BucketlistItems(Resource):

    """Update and Delete BucketlistItems."""

    @token_auth.login_required
    def put(self, id, item_id):

        existing_items = BucketListItem.query.filter_by(bucketlist_id=id).all()

        # Updates a single bucketlist item
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        parser.add_argument('done', type=str, required=False, location='json')
        args = parser.parse_args()

        bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()
        if bucketlist:

            bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=id, id=item_id).first()

            if bucketlist_item:

                if args.done == 'No':
                    args.done = False
                elif args.done == 'Yes':
                    args.done = True
                else:
                    return {'message': "Use either 'Yes' or 'No' for done"}, 400

                if args.name in existing_items.name:
                    return {'message': 'Item with that name already exists in this bucketlist.'}, 409
                bucketlist_item.name = args.name
                bucketlist_item.done = args.done

                try:
                    DB.session.commit()
                    return {'message': 'Changes have been made succesfully.'}, 200
                except Exception:
                    DB.session.rollback()
                    return {'message': 'An error occured during saving.'}, 500

            return {'message': 'An item with that id was not found.'}, 404

        return {'message': 'You are not authorized to edit this bucketlist item.'}, 401

    @token_auth.login_required
    def delete(self, id, item_id):
        # Deletes a single bucketlist item
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=g.user.id).first()
        if bucketlist:

            try:
                BucketListItem.query.filter_by(id=item_id).delete()
                DB.session.commit()
                return {'message': 'Item has been deleted successfully.'}, 200
            except Exception:
                DB.session.rollback()
                return {'message': 'An error occured during saving.'}, 200

        return {'message': "You are not authorized to delete this item"}, 401
