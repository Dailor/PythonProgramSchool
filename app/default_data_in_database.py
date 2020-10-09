from app.models import db_session
from app.models.__all_models import User, Admin
from app import app


def add_default_admin():
    session = db_session.create_session()
    user = session.query(User).first()

    if user:
        return

    user = User()
    user.name = "Admin"
    user.surname = "Admin"
    user.email = app.config["ADMIN_DEFAULT_EMAIL"]
    user.set_password(app.config["ADMIN_DEFAULT_PASSWORD"])

    admin_user = Admin()
    user.admin = admin_user

    session.add(user)
    session.commit()


def add_default_data():
    add_default_admin()


add_default_data()
