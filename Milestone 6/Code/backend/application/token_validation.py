from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"message": "Missing or invalid token"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired"}), 401
