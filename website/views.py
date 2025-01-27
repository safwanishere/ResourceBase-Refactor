from flask import Blueprint, render_template,request
import sqlite3

views = Blueprint('views', __name__)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/branch')
def branch():
    branch_name = request.args.get('branchName')

    if not branch_name:
        return "Error: 'branchName' parameter is required!", 400

    connection = get_db_connection()
    cursor = connection.cursor()

    
    query = """
        SELECT code, branch, semester, course_name, type
        FROM courses
        WHERE branch = ?
        ORDER BY semester ASC;
    """
    cursor.execute(query, (branch_name,))
    courses = cursor.fetchall()
    connection.close()

    semesters = {}
    for course in courses:
        semester = course['semester']
        if semester not in semesters:
            semesters[semester] = []
        semesters[semester].append(course)

    return render_template('branch.html', branch_name=branch_name, semesters=semesters)


@views.route('/course')
def course():
    courseCode = request.args.get('code')

    dbCon = sqlite3.connect("database.db")
    cursor = dbCon.cursor()

    cursor.execute("SELECT course_name, category, title, path FROM files WHERE course_code = ?;", (courseCode,))
    res = cursor.fetchall()

    return "course"




@views.route('/contact')
def contact():
    return "contact"