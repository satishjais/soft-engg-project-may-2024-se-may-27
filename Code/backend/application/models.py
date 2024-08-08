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
    courses =  db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))

class Course(db.Model):
    __tablename__ = 'Courses'
    CourseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseName = db.Column(db.String, nullable=False)
    CourseDescription = db.Column(db.String)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Assignment(db.Model):
    __tablename__ = 'Assignments'
    AssignmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    Title = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)
    DueDate = db.Column(db.Date)
    MaxScore = db.Column(db.Integer)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Lecture(db.Model):
    __tablename__ = 'Lectures'
    LectureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    LectureTitle = db.Column(db.String, nullable=False)
    LectureLink = db.Column(db.String, nullable=False)
    LectureDate = db.Column(db.Date)
    Description = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    __tablename__ = 'Announcements'
    AnnouncementID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    Title = db.Column(db.String, nullable=False)
    Content = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class CourseDocs(db.Model):
    __tablename__ = 'Documents'
    DocID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    DocName = db.Column(db.String, nullable=False)
    DocLink = db.Column(db.String, nullable=False)

class SupportRequest(db.Model):
    __tablename__ = 'SupportRequests'
    RequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    RequestDetails = db.Column(db.String)
    RequestStatus = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)