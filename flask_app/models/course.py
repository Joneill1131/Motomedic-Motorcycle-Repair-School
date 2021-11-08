from flask_app.config.mysqlconnection import connectToMYSQL
from flask_app import app
from flask import flash
from flask_app.models import student


class Course:
    def __init__(self, data):
        self.id = data['id']
        self.course_name = data['course_name']
        self.course_start_month = data['course_start_month']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM courses;"
        results = connectToMYSQL('students').query_db(query)
        courses = []
        if len(results) == 0:
            return courses
        else:
            for course in results:
                courses.append(cls(courses))
            return courses

    @classmethod
    def get_all_complete(cls):
        query = "SELECT * FROM courses JOIN students ON courses.student_id = students.id;"
        results = connectToMYSQL('students').query_db(query)
        courses = []
        if len(results) == 0:
            return courses
        else:
            for course in results:
                student_data = {
        'id' : course['students.id'],
        'first_name' : course['first_name'],
        'last_name' :  course['last_name'],
        'email' : course['email'],
        'password' : course['password'],
        'created_at' : course['users.created_at'],
        'updated_at' : course['users.updated_at']
                }
                creator = student.Student(student_data)
                new_course = cls(course)
                new_course.creator = creator
                courses.append(new_course)
            return courses
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM courses WHERE student_id = %(id)s;"
        results = connectToMYSQL('students').query_db(query,data)
        courses = []
        for course in results:
            courses.append(cls(course))
        return courses

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO courses ( course_name, course_start_month , created_at, updated_at, student_id ) VALUES ( %(course_name)s , %(course_start_month)s , NOW() , NOW(), %(student_id)s );"
        return connectToMYSQL('students').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM courses WHERE id = %(id)s;"
        results = connectToMYSQL('students').query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE courses SET course_name=%(course_name)s, course_start_month= %(course_start_month)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMYSQL('students').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM courses WHERE id = %(id)s;"
        return connectToMYSQL('students').query_db(query,data)

    @staticmethod
    def validate_course(course):
        is_valid = True
        if len(course['course_name']) < 2:
            flash('Course names must be at least 2 characters.')
            is_valid = False
        if len(course['course_start_month']) < 2:
            flash('Course start month must be at least 2 characters long')
            is_valid = False
        return is_valid