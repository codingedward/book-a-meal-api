from functools import wraps
from app.models import User
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity


def current_user():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        raise Exception('Authentication: current user not found')


def admin_jwt_required(fn):
    @wraps(fn)
    @jwt_required
    def wrapper(*args, **kwargs):
        if not current_user().is_caterer():
            abort(
                make_response(
                    jsonify({'message': 'Unauthorized access to a non-admin'}),
                    401
                )
            )
        fn(*args, **kwargs)
    return wrapper
