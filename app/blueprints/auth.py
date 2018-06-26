"""This handles user authentication"""

from app.validation import validate
from app.middlewares.auth import admin_auth, user_auth
from app.models import User, Blacklist
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                get_raw_jwt)
from app.requests.auth import LoginRequest, RegisterRequest

auth = Blueprint('auth', __name__)


@auth.route('/api/v1/auth/signup', methods=['POST'])
@validate(RegisterRequest)
def register():
    """Register a user using their username, email and
    password"""
    user = User.create(request.json)
    return jsonify({
        'success': True,
        'message': 'Successfully registered account.',
        'data': {
            'user': user.to_dict(),
        }
    }), 201


@auth.route('/api/v1/auth/login', methods=['POST'])
@validate(LoginRequest)
def login():
    """Logs in a user using JwT and responds with an access token"""

    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.validate_password(request.json['password']):
        return jsonify({
            'success': False,
            'message': 'Invalid credentials',
        }), 400

    token = create_access_token(identity=request.json['email'])
    return jsonify({
        'success': True,
        'message': 'Successfully logged in',
        'data': {
            'access_token': token,
            'user': user.to_dict()
        }
    }), 200


@auth.route('/api/v1/auth/get', methods=['GET'])
@user_auth
def get_user():
    """Returns the authencicated users details"""

    user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        'success': True,
        'message': 'Successfully retrieved user',
        'data': {
            'user': user.to_dict()
        }
    }), 200


@auth.route('/api/v1/auth/logout', methods=['DELETE'])
@user_auth
def logout():
    """Logs out currently logged in user by adding the JWT to a blacklist"""

    jti = get_raw_jwt()['jti']
    blacklist = Blacklist(token=jti)
    blacklist.save()
    return jsonify({
        'success': True,
        'message': 'Successfully logged out.'
    }), 200
