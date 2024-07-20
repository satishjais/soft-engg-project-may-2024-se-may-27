from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seproject.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Role = db.Column(db.String, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

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
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    RequestDetails = db.Column(db.String)
    RequestStatus = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    __tablename__ = 'Profiles'
    ProfileID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    FullName = db.Column(db.String)
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    SocialProfileLinks = db.Column(db.String)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Content(db.Model):
    __tablename__ = 'Content'
    ContentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdminID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Title = db.Column(db.String, nullable=False)
    ContentType = db.Column(db.String)
    ContentPath = db.Column(db.String)
    UploadedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = 'Admins'
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    AdminRole = db.Column(db.String, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
