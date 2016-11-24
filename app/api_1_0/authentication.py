# -*- coding: utf-8 -*-
from flask import g
from flask_security import AnonymousUser
from flask_httpauth import HTTPBasicAuth

from . import api
from app.api_1_0.errors import unauthorized
from .errors import forbidden
from app.models import User

from flask_jwt import JWT, jwt_required, current_identity

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.route('/token')
@jwt_required()
def get_token():
    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('Invalid credentials')
    expiration = 3600
    return {'token': g.current_user.generate_auth_token(expiration=expiration), 'expiration': expiration}


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')



