from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hadfhdfadfj"

    from .views import views
    from .admin import admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin/")

    return app