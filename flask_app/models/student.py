from flask_app.config.mysqlconnection import connectToMYSQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

class Student:
    db = "students"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name =  data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.courses = []

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO students ( first_name, last_name, email , password, created_at, updated_at ) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s, NOW() , NOW() );"
        return connectToMYSQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM students;"
        results = connectToMYSQL(cls.db).query_db(query)
        students = []
        for student in results:
            students.append( cls(student))
        return students
    
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM students WHERE students.email = %(email)s;"
        results = connectToMYSQL(cls.db).query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0]) 
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM students WHERE id = %(id)s;"
        results = connectToMYSQL(cls.db).query_db(query,data)
        student = cls(results[0])
        return student

    @staticmethod
    def validate_registration(student):
        is_valid = True
        query = "SELECT * FROM students WHERE email = %(email)s;"
        results = connectToMYSQL('students').query_db(query,student)
        if len(results) >= 1:
            flash('Email already taken')
            is_valid = False
        if len(student['first_name']) < 2:
            flash('first name must be at least 2 characters.')
        if len(student['last_name']) < 2:
            flash('last name must be at least 2 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(student['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(student['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid = False
        if not student['password'] == student['confirm_password']:
            flash('Passwords must match')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(student):
        is_valid = True
        e_data = { 'email' : student['email']}
        student_from_db = Student.get_one_by_email(e_data)
        if not student_from_db:
            flash('Invalid Email/Password')
            is_valid = False
        elif not bcrypt.check_password_hash(student_from_db.password, student['password']):
            flash("Invalid Email/Password")
            is_valid = False
        if not EMAIL_REGEX.match(student['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(student['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid = False
        return is_valid


