import pytest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from application import app, db
from application.models import User, Course, Assignment, Announcement, Lecture, CourseDocs
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_api(client: FlaskClient):
    response = client.post('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the App"}

def test_register_new_user(client: FlaskClient):
    data = {
        "username": "iitmbsstudent",
        "password": "iitmbs123",
        "email": "student@ds.study.iitm.ac.in",
        "mob": "1234567890",
        "name": "Soft Engg Student", ###############################################
        "courses": ["python"]
    }
    response = client.post('/register', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully", "code": 201}

def test_register_existing_user(client: FlaskClient):
    # First, register a user
    data = {
        "username": "iitmbsstudent",
        "password": "iitmbs123",
        "email": "student@ds.study.iitm.ac.in",
        "mob": "1234567890",
        "name": "Soft Engg Student"
    }
    client.post('/register', json=data)
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert response.json == {"error": "This username is already taken", "code": 400}

def test_valid_login(client: FlaskClient):
    data = {
        "username": "iitmbsstudent",
        "password": "iitmbs123",
        "email": "student@ds.study.iitm.ac.in",
        "mob": "1234567890",
        "name": "Soft Engg Student"
    }
    client.post('/register', json=data)

    # Now, test login
    login_data = {
        "username": "iitmbsstudent",
        "password": "iitmbs123"
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    assert "token" in response.json

def test_invalid_login(client: FlaskClient):
    login_data = {
        "username": "invalidiitmuser",
        "password": "wrongiitmbspassword"
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid credentials", "code": 400}

def test_dashboard_api(client: FlaskClient):
    # We are assuming user with id 1 exists
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert "dashboard" in response.json

def test_study_api(client: FlaskClient):
    response = client.get('/study')
    assert response.status_code == 200
    assert "study" in response.json

def test_create_new_course(client: FlaskClient):
    data = {
        "course_name": "Python",
        "course_description": "Python is a Programming Langyage.",
        "start_date": "2024-05-28",
        "end_date": "2024-09-01"
    }
    response = client.post('/study', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Course created successfully", "code": 201}

def test_fetch_lectures(client: FlaskClient):
    # We are assuming course with id 1 exists
    response = client.get('/study/lectures')
    assert response.status_code == 200
    assert "lectures" in response.json

def test_create_new_lecture(client: FlaskClient):
    data = {
        "lecture_title": "Introduction to Python",
        "lecture_link": "https://www.youtube.com/watch?v=8ndsDXohLMQ&list=PLZ2ps__7DhBb2cXAu5PevO_mzgS3Fj3Fs",
        "lecture_date": "2024-05-28",
        "lecture_description": "Introductory lecture to Python Programming Language"
    }
    response = client.post('/study/lectures', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Lecture created successfully", "code": 201}

def test_fetch_user_profile(client: FlaskClient):
    response = client.get('/profile')
    assert response.status_code == 200
    assert "profile" in response.json

def test_fetch_course_documents(client: FlaskClient):
    # We are assuming course with id 1 exists
    response = client.get('/study/course_docs')
    assert response.status_code == 200
    assert "course_docs" in response.json

def test_add_new_document(client: FlaskClient):
    data = {
        "doc_title": "Transcript",
        "doc_link": "https://drive.google.com/file/d/1kYbJ8wTIkokMO3rZz0RZLVnRYCaMhBsJ/view?usp=sharing"
    }
    response = client.post('/study/course_docs', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Document created successfully", "code": 201}

def test_fetch_practice_assignments(client: FlaskClient):
    response = client.get('/study/practice')
    assert response.status_code == 200
    assert "practice_assignments" in response.json

def test_fetch_graded_assignments(client: FlaskClient):
    response = client.get('/study/graded')
    assert response.status_code == 200
    assert "graded_assignments" in response.json

def test_execute_python_code(client: FlaskClient):
    code = {
        "code": "print('Hello, World!')"
    }
    response = client.post('/execute', json=code)
    assert response.status_code == 200
    assert response.json['output'] == "Hello, World!\n"



    
