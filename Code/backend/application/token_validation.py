import application.errors as errors
import datetime
import jwt
from flask import current_app as app, jsonify, request
from functools import wraps

def validate_jwt():
    if not 'Authorization' in request.headers:
        raise errors.AuthorizationTokenRequired
    user = None
    token = request.headers['Authorization'].split(' ')[1]
    try:
        user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise errors.JwtTokenExpired
    except jwt.InvalidTokenError:
        raise errors.InvalidJwtToken

    return(user)

def generate_jwt(user):
    user=user['user']
    token=jwt.encode({'id':user.id, 'role': user.role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)},app.config['SECRET_KEY'], algorithm="HS256" )

    return(token)

def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return jsonify({"error": "Authorization required"})
        user = None
        token = request.headers['Authorization'].split(' ')[1]
        try:
            user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return func(user, *args, **kwargs)
    return decorated_func