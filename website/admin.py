import sqlite3
from flask import Blueprint, session, redirect, render_template, request
from functools import wraps

# helper functions
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/admin/login")
        return f(*args, **kwargs)

    return decorated_function



admin = Blueprint('admin', __name__)

@admin.route('/login', methods=["GET", "POST"])
def login():
    
    # forget any user
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return redirect("/admin/login")

        elif not request.form.get("password"):
            return redirect("/admin/login")

        # Query database for username
        dbcon = sqlite3.connect("database.db")
        cursor = dbcon.cursor()

        cursor.execute(
            f"SELECT * FROM admins WHERE username = ?;", (request.form.get('username'),)
        )
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or rows[0][2] != request.form.get('password'):
            print()
            print("invalid username or password")
            print()
            return redirect("/admin/login")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        cursor.close()
        dbcon.close()

        # Redirect user to home page
        return redirect("/admin/upload")

    else:
        return render_template("login.html")


@admin.route('/logout')
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/admin/login")


@admin.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    
    if request.method == "POST":
        pass

    else:
        dbcon = sqlite3.connect("database.db")
        cursor = dbcon.cursor()

        user_id = session["user_id"]
        cursor.execute("SELECT * FROM admins WHERE ID = ?;", (user_id,))
        rows = cursor.fetchall()
        role = rows[0][3]
        
        if role == 'admin':
            cursor.execute("SELECT DISTINCT(branch) FROM courses;")
            branches = cursor.fetchall()            
            cursor.execute("SELECT DISTINCT(course_name), code, semester FROM courses;")
            courses = cursor.fetchall()
        else:
            branches = [role]
            cursor.execute("SELECT DISTINCT(course_name), code, semester FROM courses WHERE branch = ?;", (role,))
            courses = cursor.fetchall()
        
        categories =  [
            "Course Syllabus",
            "Textbooks",
            "Question Bank",
            "Lecture Slides",
            "Lecture Notes",
            "Definitions and Terminology",
            "Previous Question Papers",
            "course syllabus",
            "Lab Manual",
            "Lecture Records"
        ]

        cursor.close()
        dbcon.close()

        return render_template("upload.html", branches=branches, courses=courses, categories=categories)