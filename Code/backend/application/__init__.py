from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '7cc6619eb68e5c5f5d2ee4fc'
db = SQLAlchemy(app)
api = Api(app)
from . import models
from . import controllers

with app.app_context():
    db.create_all()