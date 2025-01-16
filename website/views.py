from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/branch')
def branch():
    return "branch"

@views.route('/course')
def course():
    return "course"

@views.route('/contact')
def contact():
    return "contact"