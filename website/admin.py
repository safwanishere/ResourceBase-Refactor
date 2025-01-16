import sqlite3
from flask import Blueprint, session, redirect, render_template, request
from .helpers import login_required

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
            f"SELECT * FROM admins WHERE username = '{request.form.get('username')}';", 
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
        return render_template("upload.html")