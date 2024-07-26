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
    LectureDate = db.Column(db.Date)
    LectureTime = db.Column(db.Time)
    Description = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    __tablename__ = 'Announcements'
    AnnouncementID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    Title = db.Column(db.String, nullable=False)
    Content = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    __tablename__ = 'Documents'
    DocumentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'))
    DocumentName = db.Column(db.String, nullable=False)
    DocumentPath = db.Column(db.String, nullable=False)
    UploadedAt = db.Column(db.DateTime, default=datetime.utcnow)

class SupportRequest(db.Model):
    __tablename__ = 'SupportRequests'
    RequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    RequestDetails = db.Column(db.String)
    RequestStatus = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Content(db.Model):
    __tablename__ = 'Content'
    ContentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdminID = db.Column(db.Integer, db.ForeignKey('Users.id'))
    Title = db.Column(db.String, nullable=False)
    ContentType = db.Column(db.String)
    ContentPath = db.Column(db.String)
    UploadedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = 'Admins'
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    AdminRole = db.Column(db.String, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)