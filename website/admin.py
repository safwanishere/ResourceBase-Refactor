import sqlite3
import os
from flask import Blueprint, session, redirect, render_template, request
from functools import wraps
from werkzeug.utils import secure_filename

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
            error = "Invalid username or password"
            return render_template("adminResponse.html", error=error, back="login")

        # Remember which user has logged in
        session["user_id"] = rows[0][1]

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
        course_name = request.form.get("course")
        category = request.form.get("category")
        fileName = secure_filename(request.form.get("fileName"))
        title = request.form.get("title")
        file = request.files['file']

        if file.filename == "":
            error = "file not uploaded"
            return render_template("adminResponse.html", error=error, back="upload")
        
        dbcon = sqlite3.connect("database.db")
        cursor = dbcon.cursor()

        cursor.execute("SELECT code, semester, type FROM courses WHERE course_name = ? LIMIT 1;", (course_name,))
        result = cursor.fetchall()[0]
        code = result[0]
        sem = result[1]
        type = result[2]

        theoryCategories = [
            "Textbooks",
            "Question Bank",
            "Lecture Slides",
            "Lecture Notes",
            "Definitions and Terminology",
            "Previous Question Papers"
        ]

        practicalCategories = [
            "Lab Manual",
            "Lab Records"
        ]

        if type == "theory" and category not in theoryCategories:
            error = f"category '{category}' does not belong to the '{type}' subject of '{course_name}'"
            return render_template("adminResponse.html", error=error, back="upload")
        elif type == "practical" and category not in practicalCategories:
            error = f"category '{category}' does not belong to the '{type}' subject of '{course_name}'"
            return render_template("adminResponse.html", error=error, back="upload")

        if sem in [1, 2]:
            year = 1
        elif sem in [3, 4]:
            year = 2
        elif sem in [5, 6]:
            year = 3
        elif sem in [7, 8]:
            year = 4

        path = f"resources/Y{year}/{code}/{fileName}.pdf"

        file.save(f"website/static/{path}")

        user = session["user_id"]

        cursor.execute("INSERT INTO files VALUES(?, ?, ?, ?, ?, ?, ?);", (code, course_name, category, title, fileName, path, user,))

        dbcon.commit()
        
        
        success = f"File '{fileName}' uploaded to '{course_name}' subject successfully"
        return render_template("adminResponse.html", success=success, back="upload")


    else:
        dbcon = sqlite3.connect("database.db")
        cursor = dbcon.cursor()

        user_id = session["user_id"]
        cursor.execute("SELECT * FROM admins WHERE username = ?;", (user_id,))
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
            "Textbooks",
            "Question Bank",
            "Lecture Slides",
            "Lecture Notes",
            "Definitions and Terminology",
            "Previous Question Papers",
            "Lab Manual",
            "Lecture Records"
        ]

        cursor.close()
        dbcon.close()

        return render_template("upload.html", branches=branches, courses=courses, categories=categories)
    


@admin.route('/announce', methods=["GET", "POST"])
@login_required
def announce():

    if request.method == "POST":
        announcement = request.form.get("announcement")
        color = request.form.get("color")

        try: 
            dbCon = sqlite3.connect("database.db")
            cursor = dbCon.cursor()
            cursor.execute("INSERT INTO announcements VALUES (?,?);", (announcement, color,))
            dbCon.commit()
            return redirect("/")
        except:
            return "error"
    
    else:
        user = session["user_id"]

        dbCon = sqlite3.connect("database.db")
        cursor = dbCon.cursor()

        cursor.execute("SELECT role FROM admins WHERE username = ?;", (user,))
        role = cursor.fetchall()[0][0]

        if role == 'admin':
            dbCon.close()
            return render_template("announce.html")
        
        else:
            dbCon.close()
            return "access denied"
        
@admin.route('/delete', methods=["GET", "POST"])
@login_required
def delete():

    if request.method == "POST":
        name = request.form.get("name")
        dbCon = sqlite3.connect("database.db")
        cursor = dbCon.cursor()

        cursor.execute("SELECT path FROM files WHERE name = ?", (name,))
        path = cursor.fetchall()[0][0]
        path = f"website/static/{path}"

        if os.path.exists(path):
            os.remove(path)

        cursor.execute("DELETE FROM files WHERE name = ?", (name,))
        dbCon.commit()

        return redirect("/")

    else:
        user = session["user_id"]

        dbCon = sqlite3.connect("database.db")
        cursor = dbCon.cursor()

        cursor.execute("SELECT role FROM admins WHERE username = ?;", (user,))
        role = cursor.fetchall()[0][0]

        if role == 'admin':
            cursor.execute("SELECT name FROM files ORDER BY ROWID DESC;")
            names = cursor.fetchall()
            return render_template("delete.html", names=names)
        
        else:
            dbCon.close()
            return "access denied"