import os
from flask import request, jsonify, make_response, send_file
from flask_restful import Resource
from application.models import User, Course, Assignment, Announcement, Lecture, CourseDocs
from application import db, api, app
from flask_bcrypt import Bcrypt
import datetime
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from datetime import datetime

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
            courses = data.get('courses')

            if not (username and password and email and mob and name):
                return jsonify({'error': 'All fields are required', 'code': 400})
            print('gtg')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({'error': 'This username is already taken', 'code': 400})
            #courses=Course.query.filter_by(CourseID=courses).first()
            print(courses)

            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                mob=mob,
                name=name,
                courses=courses,
                first_login_time=datetime.utcnow()
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
            return jsonify({'error': 'e' , 'code': 500})


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
            access_token = create_access_token(identity={'user_id': user_id})
            print(access_token)
            return jsonify({'token': access_token, 'code': 200, 'user_id': user_id})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)})


##################################################### DASHBOARD API ####################################################################
class Dashboard(Resource):
    @jwt_required()  # Ensure the user is authenticated
    def get(self):
        try:
            # Get the user_id from the JWT token
            current_user = get_jwt_identity()
            user_id = current_user['user_id']

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
                announcements_data = []

            # Fetch user's assignments
            try:
                assignments = Assignment.query.filter_by(user_id=user_id).all()
                deadlines_data = [
                    {assignment.Title: assignment.DueDate} for assignment in assignments
                ]
            except:
                deadlines_data = []

            # Compile dashboard data
            dashboard_data = {
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'deadlines': deadlines_data,
                'announcements': announcements_data,
            }
            print(dashboard_data)
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
                courses = Course.query.filter_by(CourseID=user.courses).first()
                # Fetch course content
                course_content = [
                    {
                        'course_id': courses.CourseID,
                        'course_name': courses.CourseName,
                        'course_description': courses.CourseDescription
                    }
                ]
            except :
                course_content ="upload karenge"
                print(course_content)

            return jsonify({'study': course_content, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

    def post(self):
        try:
            data = request.get_json()
            course_name = data.get('course_name')
            course_description = data.get('course_description')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            new_course = Course(
                CourseName=course_name,
                CourseDescription=course_description,
                StartDate=start_date,
                EndDate=end_date,
                CreatedAt=datetime.utcnow()
            )
            db.session.add(new_course)
            db.session.commit()

            return jsonify({'message': 'Course created successfully', 'code': 201})

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return jsonify({'error': str(e), 'code': 500})


##################################################### LECTURES API ####################################################################
class Lectures(Resource): #user_id to be passed later
    def get(self):
        try:
            course_id =1
            #to be done: Login through JWT and pass user_id
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found', 'code': 404})
            # Fetch user's courses and calculate progress
            try :
                lectures = Lecture.query.filter_by(CourseID=course.CourseID).all()
                lectures_data=[]
                for l in lectures:
                    lectures_data.append({
                        'lecture_id': l.LectureID,
                        'lecture_title': l.LectureTitle,
                        'lecture_link': l.LectureLink,
                        'lecture_date': l.LectureDate,
                        'description': l.Description
                    })
            except :
                lectures_data ="upload karenge"
            return jsonify({'lectures': lectures_data, 'code': 200})
        except Exception as e:
            return jsonify({'error': 'ruk', 'code': 500})

    def post(self):
        try:
            data = request.get_json()
            lecture_title = data.get('lecture_title')
            lecture_link = data.get('lecture_link')
            lecture_date = data.get('lecture_date')
            lecture_description = data.get('lecture_description')

            lecture_date = datetime.strptime(lecture_date, '%Y-%m-%d')
            new_lecture = Lecture(
                CourseID=1,
                LectureTitle=lecture_title,
                LectureLink=lecture_link,
                LectureDate=lecture_date,
                Description=lecture_description,
                CreatedAt=datetime.utcnow()
            )
            db.session.add(new_lecture)
            db.session.commit()

            return jsonify({'message': 'Lecture created successfully', 'code': 201})

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return jsonify({'error': str(e), 'code': 500})


##################################################### PROFILE API ####################################################################
class Profile(Resource):
    def get(self): #user_id to be passed later
        try:
            user_id = 1
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})
            
            
            # Fetch user's courses
            try:
                courses = Course.query.filter_by(id=user.course).all()
                subjects_taken = [course.CourseName for course in courses]
            except:
                subjects_taken = 'Course nahi hai'
            
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


##################################################### COURSEDOCS API ####################################################################
class CourseDocuments(Resource):

    def get(self):
        try:
            course_id =1
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found', 'code': 404})

            documents = CourseDocs.query.filter_by(CourseID=course_id).all()
            for document in documents:
                documents_data = [
                    {
                        'document_name': document.DocName,
                        'document_link': document.DocLink,
                    }
                ]

            return jsonify({'course_docs': documents_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500})

    def post(self):
        try:
            data = request.get_json()
            doc_title = data.get('doc_title')
            doc_link = data.get('doc_link')

            new_doc = CourseDocs(
                CourseID=1,
                DocName=doc_title,
                DocLink=doc_link
            )
            db.session.add(new_doc)
            db.session.commit()

            return jsonify({'message': 'Document created successfully', 'code': 201})

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return jsonify({'error': str(e), 'code': 500})


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


#class Downloads(Resource):

#First Priority
api.add_resource(Home, "/")
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Dashboard, "/dashboard")


#Second Priority
api.add_resource(Study, "/study")
# api.add_resource(Downloads, "/downloads")
# api.add_resource(Forum, "/forum") not needed as am API
api.add_resource(Profile, "/profile")
# api.add_resource(Deadlines, "/deadlines")
# api.add_resource(Announcements, "/announcements")


#Third Priority
# api.add_resource(Content, "/study/content")
api.add_resource(CourseDocuments, "/study/course_docs")
api.add_resource(Practice, "/study/practice")
api.add_resource(Graded, "/study/graded")
api.add_resource(Lectures, "/study/lectures")
# api.add_resource(Scores, "/scores")
# api.add_resource(Payments, "/profile/payments")
# api.add_resource(ATS, "/profile/ats")
# api.add_resource(Support, "/profile/support")