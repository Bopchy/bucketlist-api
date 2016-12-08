from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask_httpauth import HTTPTokenAuth

from bucketlist_models import Users
from config import Config


token_auth = HTTPTokenAuth(scheme='Token')
jwt = Serializer(Config.SECRET_KEY)


@token_auth.verify_token
def verify_token(token):
    # Decodes the token to get the user that was assigned token
    # Ensures that token is authentic before decoding it and assiging
    # user with the token's request context (g).

    # g.user = None
    try:
        data = jwt.loads(token)
    except SignatureExpired:
        return ' This token has expired.'
    except BadSignature:
        return 'Invalid signature.'

    tokened_user = Users.query.get(data['id'])

    if tokened_user:
        g.user = tokened_user
        return g.user
    return False
