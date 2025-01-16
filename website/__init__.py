from flask import Flask, session
from flask_session import Session

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hadfhdfadfj"

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from .views import views
    from .admin import admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin/")

    return app