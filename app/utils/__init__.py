from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity


def current_user():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        raise Exception('Authentication: current user not found')
