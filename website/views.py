from flask import Blueprint, render_template,request
import sqlite3

views = Blueprint('views', __name__)

BRANCHES = {
    "cse": "Computer Science Engineering",
    "aiml": "Artificial Intelligence and Machine Learning",
    "cs": "Cyber Security",
    "ds": "Data Science",
    "aero": "Aeronautical Engineering",
    "civil": "Civil Engineering",
    "mech": "Mechanical Engineering",
    "ece": "Electronics and Communications Engineering",
    "eee": "Electrical and Electronics Engineering"
}

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

    return render_template('branch.html', branch_name=BRANCHES[branch_name], semesters=semesters)


@views.route('/course')
def course():
    courseCode = request.args.get('code')

    dbCon = sqlite3.connect("database.db")
    cursor = dbCon.cursor()

    cursor.execute("SELECT course_name, category, title, path, name FROM files WHERE course_code = ? ORDER BY category, title;", (courseCode,))
    res = cursor.fetchall()
    
    try:
        courseName = res[0][0]
    except:
        cursor.execute("SELECT course_name FROM courses WHERE code = ? LIMIT 1;", (courseCode,))
        try:
            courseName = cursor.fetchall()[0][0]
            return render_template(
                "course.html",
                courseName=courseName,
                courseCode=courseCode
            )
        except:
            return render_template(
                "course.html",
                error="course doesn't exist"
            )

    cursor.execute("SELECT type FROM courses WHERE code = ?;", (courseCode,))
    type = cursor.fetchall()[0][0]

    if type == "theory":
        textbooks = []
        questionBank = []
        lectureSlides = []
        lectureNotes = []
        dt = []
        pyq = []

        for row in res:
            if row[1] == "Textbooks":
                textbooks.append(row)
            elif row[1] == "Question Bank":
                questionBank.append(row)
            elif row[1] == "Lecture Slides":
                lectureSlides.append(row)
            elif row[1] == "Lecture Notes":
                lectureNotes.append(row)
            elif row[1] == "Previous Question Papers":
                pyq.append(row)
            elif row[1] == "Definitions and Terminology":
                dt.append(row)
        
        return render_template(
            "course.html",
            courseName=courseName,
            courseCode=courseCode,
            textbooks=textbooks,
            questionBank=questionBank,
            lectureSlides=lectureSlides,
            lectureNotes=lectureNotes,
            dt=dt,
            pyq=pyq,
            type=type
        )
                

    elif type == "practical":
        labManual = []
        labRecords = []

        for row in res:
            if row[1] == "Lab Manual":
                labManual.append(row)
            elif row[1] == "Lab Records":
                labRecords.append(row)

        return render_template(
            "course.html",
            labManual=labManual,
            labRecords=labRecords,
            courseName=courseName,
            courseCode=courseCode,
            type=type
        )




@views.route('/contact', methods=["GET", "POST"])
def contact():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        dbCon = sqlite3.connect("database.db")
        cursor = dbCon.cursor()

        cursor.execute(
            "INSERT INTO contact (name, email, subject, message, datetime) VALUES (?,?,?,?,CURRENT_TIMESTAMP);",
            (name, email, subject, message,)
        )

        dbCon.commit()

        return render_template("contact.html", sent=True)
    
    else:
        return render_template("contact.html")