from flask import render_template, request, redirect, session, flash
from flask_app.models.course import Course
from flask_app.models.student import Student
from flask_app import app

# @app.route('/dashboard')
# def dashboard_page():
#     if not 'student_id' in session:
#         return redirect('/')
#     data = {
#         'id': session['student_id']
#     }
#     return render_template('dashboard.html', classes = Class.get_all_complete(), student=Student.get_by_id(data))
    
@app.route('/dashboard')
def my_course_page():
    if not 'student_id' in session:
        return redirect('/')
    data = {
        'id': session['student_id']
    }
    return render_template('dashboard.html', courses = Course.get_by_id(data), student=Student.get_by_id(data))

@app.route('/courses/edit/<int:course_id>')
def edit_course(course_id):
    if not 'student_id' in session:
        return redirect('/')
    data = {
        'id': course_id
    }
    student_data = {
        'id': session['student_id']
    }
    return render_template("change_course_date.html", course = Course.get_one(data), student = Student.get_by_id(student_data))

@app.route('/courses/new')
def course_new():
    if not 'student_id' in session:
        return redirect('/')
    data = {
        "id" : session['student_id']
    }
    return render_template("add_course.html", student=Student.get_by_id(data))

@app.route('/add_course', methods=['POST'])
def add_course():
    if not 'student_id' in session:
        return redirect('/')
    if not Course.validate_course(request.form):
        return redirect('/courses/new')
    data = {
        "course_name": request.form["course_name"],
        "course_start_month": request.form["course_start_month"],
        "student_id": session['student_id']
    }
    Course.save(data)
    return redirect('/dashboard')


@app.route('/update/<int:course_id>', methods=['POST'])
def update(course_id):
    if not 'student_id' in session:
        return redirect('/')
    if not Course.validate_course(request.form):
        return redirect(f'/courses/edit/{course_id}')
    data = {
        "id": course_id,
        "course_name": request.form["course_name"],
        "course_start_month": request.form["course_start_month"],
        "student_id": session['student_id']
    }
    Course.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:course_id>')
def destroy_course(course_id):
    if 'student_id' not in session:
        return redirect('/logout')
    data = {
        "id": course_id
    }
    Course.destroy(data)
    return redirect('/dashboard')