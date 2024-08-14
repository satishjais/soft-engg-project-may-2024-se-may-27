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

            # Fetch user based on the provided username
            user = User.query.filter_by(username=username).first()

            # Check if the user exists and the password is correct
            if not user or not bcrypt.check_password_hash(user.password, password):
                return jsonify({'error': 'Invalid credentials', 'code': 400})

            # Extract user ID and role
            user_id = user.id
            user_role = user.role

            # Create access token with user ID and role included in the identity
            access_token = create_access_token(identity={'user_id': user_id, 'role': user_role})
            print(user_role)

            # Return the token, user ID, and role in the response
            return jsonify({'token': access_token, 'code': 200, 'user_id': user_id, 'role': user_role})

        except Exception as e:
            # Handle any unexpected errors
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
class Study(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user_id = current_user['user_id']
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            if user.role == 'Admin':
                courses = Course.query.all()
                if not courses:
                    return jsonify({'study': [], 'code': 200})

                course_content = [
                    {
                        'course_id': course.CourseID,
                        'course_name': course.CourseName,
                        'course_description': course.CourseDescription,
                        'start_date': course.StartDate,
                        'end_date': course.EndDate,
                    }
                    for course in courses
                ]
                return jsonify({'study': course_content, 'code': 200})

            courses = Course.query.filter(Course.CourseID.in_(user.courses)).all()
            if not courses:
                return jsonify({'study': [], 'code': 200})

            course_content = [
                {
                    'course_id': course.CourseID,
                    'course_name': course.CourseName,
                    'course_description': course.CourseDescription
                }
                for course in courses
            ]
            return jsonify({'study': course_content, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)})

    @jwt_required()
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
            db.session.rollback()
            return jsonify({'error': str(e), 'code': 500})

    @jwt_required()
    def delete(self, course_id):
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found', 'code': 404})

            db.session.delete(course)
            db.session.commit()

            return jsonify({'message': 'Course deleted successfully', 'code': 200})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e), 'code': 500})

##################################################### LECTURES API ####################################################################
class Lectures(Resource):
    @jwt_required()
    def get(self):
        try:
            courses = Course.query.all()
            if not course:
                return jsonify({'error': 'Course not found', 'code': 404})
            lectures_data=[]
            try:
                for course in courses:
                    lectures = Lecture.query.filter_by(CourseID=course.CourseID).all()
                    lectures_data1 = []
                    for l in lectures:
                        lectures_data1.append({
                            'course_name': course.CourseName,
                            'lecture_id': l.LectureID,
                            'lecture_title': l.LectureTitle,
                            'lecture_link': l.LectureLink,
                            'lecture_date': l.LectureDate.strftime('%Y-%m-%d'),
                            'description': l.Description,
                        })
                    lectures_data.append(lectures_data1)
            except:
                lectures_data=['']
            return jsonify({'lectures': lectures_data, 'courses': courses, 'code': 200})
        except Exception as e:
            return jsonify({'error': str(e), 'code': 500})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            course_id = data.get('course_id')
            lecture_title = data.get('lecture_title')
            lecture_link = data.get('lecture_link')
            lecture_date = data.get('lecture_date')
            lecture_description = data.get('lecture_description')

            if not course_id or not lecture_title or not lecture_link or not lecture_date:
                return jsonify({'error': 'Missing required fields', 'code': 400})

            lecture_date = datetime.strptime(lecture_date, '%Y-%m-%d')
            new_lecture = Lecture(
                CourseID=course_id,
                LectureTitle=lecture_title,
                LectureLink=lecture_link,
                LectureDate=lecture_date,
                Description=lecture_description,
                CreatedAt=datetime.utcnow()
            )
            db.session.add(new_lecture)
            db.session.commit()

            return jsonify({
                'message': 'Lecture created successfully',
                'new_lecture': {
                    'lecture_id': new_lecture.LectureID,
                    'lecture_title': new_lecture.LectureTitle,
                    'lecture_link': new_lecture.LectureLink,
                    'lecture_date': new_lecture.LectureDate.strftime('%Y-%m-%d'),
                    'description': new_lecture.Description
                },
                'code': 201
            })
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
                documents = CourseDocs.query.join(Course, CourseDocs.CourseID == Course.CourseID).filter(Course.user_id == user_id).all()
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

##################################################### PRACTICE ASSIGNMENT API ####################################################################
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


##################################################### GRADED ASSIGNMENT API ####################################################################
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


##################################################### DASHBOARD ADMIN API ####################################################################
class DashboardAdmin(Resource):
    print('done')
    @jwt_required()  # Ensure the user is authenticated
    def get(self):
        try:
            # Get the user_id and role from the JWT token
            current_user = get_jwt_identity()
            user_id = current_user['user_id']
            user_role = current_user['role']
            # Ensure that only admin users can access this dashboard
            if user_role != 'Admin':
                return jsonify({'error': 'Access forbidden: Admins only', 'code': 403})

            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found', 'code': 404})

            # Fetch counts for the dashboard
            total_users = User.query.count()
            print(total_users)
            total_courses = Course.query.count()
            total_assignments = Assignment.query.count()
            total_lectures = Lecture.query.count()
            total_announcements = Announcement.query.count()
            total_docs = CourseDocs.query.count()

            # Fetch all announcements
            announcements = Announcement.query.all()
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

            # Fetch all assignments and their deadlines
            assignments = Assignment.query.all()
            deadlines_data = {assignment.Title: assignment.DueDate for assignment in assignments}

            # Compile the dashboard data
            dashboard_data = {
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'total_users': total_users,
                'total_courses': total_courses,
                'total_assignments': total_assignments,
                'total_lectures': total_lectures,
                'total_announcements': total_announcements,
                'total_docs': total_docs,
                'deadlines': deadlines_data,
                'announcements': announcements_data,
            }

            return jsonify({'dashboard': dashboard_data, 'code': 200})

        except Exception as e:
            return jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)})



api.add_resource(Home, "/")
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Dashboard, "/dashboard")
api.add_resource(DashboardAdmin, "/dashboard/admin")
api.add_resource(Study, "/study", "/study/<int:course_id>")
api.add_resource(Profile, "/profile")
api.add_resource(CourseDocuments, "/study/course_docs")
api.add_resource(Practice, "/study/practice")
api.add_resource(Graded, "/study/graded")
api.add_resource(Lectures, "/study/lectures")
# api.add_resource(Downloads, "/downloads")
# api.add_resource(Forum, "/forum") not needed as am API
# api.add_resource(Deadlines, "/deadlines")
# api.add_resource(Announcements, "/announcements")
# api.add_resource(Content, "/study/content")
# api.add_resource(Scores, "/scores")
# api.add_resource(Payments, "/profile/payments")
# api.add_resource(ATS, "/profile/ats")
# api.add_resource(Support, "/profile/support")