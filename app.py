import config_app
from modules import admin
from models import db_session
from models.user import User, Role, UserRoles
from forms.login import LoginForm, LoginAnswers
from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_login.login_manager import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    errors = dict()

    if form.is_submitted():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        elif user is None:
            errors[LoginAnswers.WRONG_EMAIL[0]] = LoginAnswers.WRONG_EMAIL[1]
        else:
            errors[LoginAnswers.WRONG_PASSWORD[0]] = LoginAnswers.WRONG_PASSWORD[1]

    return render_template("login.html", form=form, **errors)


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


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

    role = Role()
    role.name = UserRoles.ADMIN

    user.roles.append(role)

    session.add(user)
    session.commit()


def blueprint_routes():
    app.register_blueprint(admin.blueprint, url_prefix="/admin")


if __name__ == '__main__':
    app.config.from_object(config_app.DevelopmentConfig)
    db_session.global_init(debug=app.config["DEBUG"])
    add_default_admin()
    blueprint_routes()
    app.run(host=app.config["HOST"], port=app.config["PORT"])
