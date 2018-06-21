from app.utils import current_user
from flask import jsonify, make_response, abort
from flask_jwt_extended import jwt_required


def user_auth(fn):
    @wraps(fn)
    @jwt_required
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    return wrapper

def admin_auth(fn):
    @wraps(fn)
    @user_auth
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
