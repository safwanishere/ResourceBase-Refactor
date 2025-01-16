from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/login')
def login():
    return "login"

@admin.route('/logout')
def logout():
    return "logout"

@admin.route('/upload')
def upload():
    return "upload"