from bapi import token_auth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from bapi import token_auth
from config import Config
from bucketlist_models import Users



@token_auth.verify_token   
def verify_auth_token(token):
    # Decodes the token to get the user that was assigned token 
    # Ensures that token is authentic before decoding it and assiging 
    # user with the token request context token authentication.
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return ' This token has expired.'
    except BadSignature:
        return 'The token provided was a bad one.'

    tokened_user = Users.query.get(data['username'])
    if tokened_user:
        g.user = tokened_user
        return True 
    return False