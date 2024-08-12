import application.errors as errors
import datetime
import jwt
from flask import current_app as app, jsonify, request
from functools import wraps

def validate_jwt():
    if 'Authorization' not in request.headers:
        return jsonify({'error': 'Authorization token is required'}), 401
    token = request.headers['Authorization'].split(' ')[1]
    try:
        user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'JWT token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid JWT token'}), 401

    return user

def generate_jwt(user):
    token = jwt.encode({
        'id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token

def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        user = validate_jwt()
        if isinstance(user, tuple):  # validate_jwt returns a tuple in case of error
            return user
        return func(user, *args, **kwargs)
    return decorated_func
