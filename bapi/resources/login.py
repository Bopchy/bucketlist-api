from flask_restful import Resource, reqparse

from bapi.bucketlist_models import Users


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
