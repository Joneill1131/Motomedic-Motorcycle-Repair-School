from flask import render_template, request, redirect, session
from flask_app.models.student import Student
from flask_app.models.course import Course
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def school_home_page():
    return render_template('index.html')

@app.route('/sign_in')
def student_sign_in():
    return render_template('signin.html')

@app.route('/courses_offered')
def courses_offered():
    return render_template('courses_offered.html')

@app.route('/sign_up')
def school_sign_up():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register_student():
    if not Student.validate_registration(request.form):
        return redirect('/sign_up')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    student_id = Student.save(data)
    session['student_id'] = student_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login_student():
    if not Student.validate_login(request.form):
        return redirect('/sign_in')
    data = {
        "email": request.form["email"],
    }
    student = Student.get_one_by_email(data)
    session['student_id'] = student.id
    return redirect('/dashboard')

@app.route('/logout')
def logout_student():
    session.clear()
    return redirect('/')


