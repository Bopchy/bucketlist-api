from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask_httpauth import HTTPTokenAuth

from config import Config
from bucketlist_models import Users


token_auth = HTTPTokenAuth(scheme='Token')
jwt = Serializer(Config.SECRET_KEY)

@token_auth.verify_token   
def verify_token(token):
    # Decodes the token to get the user that was assigned token 
    # Ensures that token is authentic before decoding it and assiging 
    # user with the token request context token authentication.
    g.user = None
    try:
        data = jwt.loads(token)
    except SignatureExpired:
        return ' This token has expired.'
    except BadSignature:
        return 'The token provided was a bad one.'

    if 'id' in data:
        tokened_user = Users.query.get(data['id'])
        if tokened_user:
            g.user = tokened_user
            return True 
        return False
    return False