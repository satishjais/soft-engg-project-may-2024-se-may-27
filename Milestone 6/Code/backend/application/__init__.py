from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '7cc6619eb68e5c5f5d2ee4fc'
db = SQLAlchemy(app)
api = Api(app)

jwt = JWTManager(app)
from . import models
from . import controllers

with app.app_context():
    db.create_all()