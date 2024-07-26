import os
from flask import request, jsonify, make_response, send_file
from flask_restful import Resource
from application.models import User, Admin, Course, Assignment, Announcement, Lecture, Document, SupportRequest, Profile, Content
from application.token_validation import validate_jwt, generate_jwt
from application import db, api, app
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt()
######################################################## HOME API ####################################################################
class Home(Resource):
    def post(self):
        return {"message": "Welcome to the App"}

##################################################### REGISTRATION API ####################################################################
class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            mob = data.get('mob')
            name = data.get('name')

            if not (username and password and email and mob and name):
                return jsonify({'error': 'All fields are required', 'code': 400})
            print('gtg')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({'error': 'This username is already taken', 'code': 400})

            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                mob=mob,
                name=name,
                first_login_time=datetime.datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()

            # if role == 'Admin':
            #     user = User.query.filter_by(username=username).first()
            #     c_id = user.id
            #     creator = Admin(user_id=c_id)
            #     db.session.add(creator)
            #     db.session.commit()

            return jsonify({'message': 'User created successfully', 'code': 201})

        except Exception as e:
            return jsonify({'error': e , 'code': 500})

##################################################### LOGIN API ####################################################################
class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            user = User.query.filter_by(username=username).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                return jsonify({'error': 'Invalid credentials', 'code': 400})
            user_id=user.id
            user_role=user.role

            token = generate_jwt({'user':user})
            return jsonify({'token': token, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)})

##################################################### DASHBOARD API ####################################################################
class Dashboard(Resource):
    def get(self):
        try:
            user_id=1
            #to be done: Login through JWT and pass user_id
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            # Fetch user's announcements
            try:
                announcements = Announcement.query.filter_by(user_id=user_id).all()
                announcements_data = [
                    {
                        'announcement_id': announcement.AnnouncementID,
                        'course_id': announcement.CourseID,
                        'title': announcement.Title,
                        'content': announcement.Content,
                        'created_at': announcement.CreatedAt
                    }
                    for announcement in announcements
                ]
            except:
                announcements_data = 'nahi hai'
            try:
                assignment=Assignment.get_all()
                deadlines_data = []
                for a in assignment:
                    deadlines_data.append({
                        a.Title: a.DueDate
                    })
            except:
                deadlines_data = 'nahi hai'
            # Compile dashboard data
            dashboard_data = {
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'deadlines': deadlines_data,
                'announcements': announcements_data,
            }

            return jsonify({'dashboard': dashboard_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})


##################################################### STUDY API ####################################################################

class Study(Resource): #user_id to be passed later
    def get(self):
        try:
            user_id =1
            #to be done: Login through JWT and pass user_id
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            # Fetch user's courses and calculate progress
            try :
                courses = Course.query.filter_by(user_id=user_id).all()
                total_courses = len(courses)
                completed_courses = sum(1 for course in courses if course.end_date and course.end_date < datetime.datetime.now())
                course_progress = (completed_courses / total_courses) * 100 if total_courses > 0 else 0

                # Fetch course content
                course_content = [
                    {
                        'course_id': course.CourseID,
                        'course_name': course.CourseName,
                        'course_description': course.CourseDescription,
                        'course_content': course.Content
                    }
                    for course in courses
                ]
            except :
                course_content ="upload karenge"
                print(course_content)

            # Fetch course documents
            try :
                course_documents = Document.query.filter(Document.CourseID.in_([course.CourseID for course in courses])).all()
                documents_data = [
                    {
                        'document_id': document.DocumentID,
                        'course_id': document.CourseID,
                        'document_name': document.DocumentName,
                        'document_path': document.DocumentPath,
                        'uploaded_at': document.UploadedAt
                    }
                    for document in course_documents
                ]
            except :
                documents_data ="doc upload karenge"
                print(documents_data)

            # Fetch graded assignments
            try :
                graded_assignments = Assignment.query.filter_by(user_id=user_id, status='graded').all()
                graded_assignments_data = [
                    {
                        'assignment_id': assignment.AssignmentID,
                        'course_id': assignment.CourseID,
                        'title': assignment.Title,
                        'description': assignment.Description,
                        'due_date': assignment.DueDate,
                        'score': assignment.Score,
                        'max_score': assignment.MaxScore,
                        'created_at': assignment.CreatedAt
                    }
                    for assignment in graded_assignments
                ]
            except :
                graded_assignments_data ="graded upload karenge"
                print(graded_assignments_data)
            # Fetch practice assignments
            try :
                practice_assignments = Assignment.query.filter_by(user_id=user_id, status='practice').all()
                practice_assignments_data = [
                    {
                        'assignment_id': assignment.AssignmentID,
                        'course_id': assignment.CourseID,
                        'title': assignment.Title,
                        'description': assignment.Description,
                        'due_date': assignment.DueDate,
                        'created_at': assignment.CreatedAt
                    }
                    for assignment in practice_assignments
                ]
            except :
                practice_assignments_data ="practice upload karenge"
                print(practice_assignments_data)
            # Compile study data
            study_data = {
                # 'course_progress': course_progress, {{{{formula based, will be modified later}}}}
                'course_content': course_content,
                'course_documents': documents_data,
                'graded_assignments': graded_assignments_data,
                'practice_assignments': practice_assignments_data
            }

            return jsonify({'study': study_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})
        
##################################################### DOWNLOADS API ####################################################################


class Downloads(Resource):

    def get(self): #user_id to be passed later
        try:
            user_id =1
            #to be done: Login through JWT and pass user_id
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            # Fetch all documents related to the user's courses
            try :
                documents = Document.query.join(Course, Document.CourseID == Course.CourseID).filter(Course.user_id == user_id).all()
                documents_data = [
                    {
                        'document_id': document.DocumentID,
                        'course_id': document.CourseID,
                        'document_name': document.DocumentName,
                        'document_path': document.DocumentPath,
                        'uploaded_at': document.UploadedAt
                    }
                    for document in documents
                ]
            except :
                documents_data = "doc data to be added"


            return jsonify({'downloads': documents_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

##################################################### PROFILE API ####################################################################

class Profile(Resource):
    
    def get(self): #user_id to be passed later
        try:
            user_id = 2
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            profile = Profile.query.filter_by(user_id=user.id).first()
            if not profile:
                return jsonify({'error': 'Profile not found', 'code': 404})

            # Fetch user's courses
            courses = Course.query.filter_by(id=user.course).all()
            subjects_taken = [course.CourseName for course in courses]

            # Compile profile data
            profile_data = {
                'first_name': user.name.split()[0],
                'last_name': user.name.split()[-1] if len(user.name.split()) > 1 else '',
                'email': user.email,
                'mob': user.mob,
                'subjects_taken': subjects_taken,
            }

            return jsonify({'profile': profile_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

class CourseDocs(Resource):
    
    def get(self, course_id):
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found', 'code': 404})

            # Fetch documents related to the course
            documents = Document.query.filter_by(CourseID=course_id).all()
            documents_data = [
                {
                    'document_id': document.DocumentID,
                    'document_name': document.DocumentName,
                    'document_path': document.DocumentPath,
                    'uploaded_at': document.UploadedAt
                }
                for document in documents
            ]

            return jsonify({'course_docs': documents_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

class Practice(Resource):
    
    def get(self, user_id):
        try:
            # Fetch practice assignments related to the user
            practice_assignments = Assignment.query.filter_by(user_id=user_id, status='practice').all()
            practice_assignments_data = [
                {
                    'assignment_id': assignment.AssignmentID,
                    'course_id': assignment.CourseID,
                    'title': assignment.Title,
                    'description': assignment.Description,
                    'due_date': assignment.DueDate,
                    'created_at': assignment.CreatedAt
                }
                for assignment in practice_assignments
            ]

            return jsonify({'practice_assignments': practice_assignments_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

class Graded(Resource):
    
    def get(self, user_id):
        try:
            # Fetch graded assignments related to the user
            graded_assignments = Assignment.query.filter_by(user_id=user_id, status='graded').all()
            graded_assignments_data = [
                {
                    'assignment_id': assignment.AssignmentID,
                    'course_id': assignment.CourseID,
                    'title': assignment.Title,
                    'description': assignment.Description,
                    'due_date': assignment.DueDate,
                    'score': assignment.Score,
                    'max_score': assignment.MaxScore,
                    'created_at': assignment.CreatedAt
                }
                for assignment in graded_assignments
            ]

            return jsonify({'graded_assignments': graded_assignments_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})


#First Priority
api.add_resource(Home, "/")
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Dashboard, "/dashboard")


#Second Priority
api.add_resource(Study, "/study")
api.add_resource(Downloads, "/downloads")
# api.add_resource(Forum, "/forum") not needed as am API
api.add_resource(Profile, "/profile")
# api.add_resource(Deadlines, "/deadlines")
# api.add_resource(Announcements, "/announcements")


#Third Priority
# api.add_resource(Content, "/study/content")
api.add_resource(CourseDocs, "/study/course_docs")
api.add_resource(Practice, "/study/practice")
api.add_resource(Graded, "/study/graded")
# api.add_resource(Scores, "/scores")
# api.add_resource(Payments, "/profile/payments")
# api.add_resource(ATS, "/profile/ats")
# api.add_resource(Support, "/profile/support")