from application import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    mob = db.Column(db.Integer, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False, default='User')
    first_login_time = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    __tablename__ = 'Courses'
    CourseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseName = db.Column(db.String, nullable=False)
    CourseDescription = db.Column(db.String)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Lecture(db.Model):
    __tablename__ = 'Lectures'
    LectureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    LectureTitle = db.Column(db.String, nullable=False)
    LectureLink = db.Column(db.String, nullable=False)
    LectureDate = db.Column(db.Date)
    Description = db.Column(db.String)
    LectureNumber = db.Column(db.Integer)
    WeekNumber = db.Column(db.Integer)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)