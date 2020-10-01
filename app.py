import config_app
from models import db_session
from models.pupil import Pupil
from models.task import TaskCheckStatus
from models.queries import tasks_count_of_pupil_for_topic
from models.user import User, Admin

from modules import admin, teacher, pupil

from forms.login import LoginForm, LoginAnswers

from api.task.task_resource import PupilSolutionForTask, PupilSolutionsListForTask

from flask import Flask, render_template, redirect, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_login.login_manager import LoginManager
from flask_restful import Api

from itertools import groupby

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.__factory.remove()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(session_id):
    session = db_session.create_session()
    return session.query(User).filter(User.session_id == session_id).first()


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


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
    if current_user.is_pupil:
        groups = current_user.pupil.groups
        if len(groups):
            return redirect(f'/pupil/groups/{groups[0].id}')
    elif current_user.is_teacher:
        return redirect('/teacher/groups')
    elif current_user.is_admin:
        return redirect('/admin/users')
    return render_template("index.html")


@app.route('/pupils/<int:pupil_id>')
def pupil_profile(pupil_id):
    if not (current_user.is_pupil is False or (current_user.is_pupil and pupil_id == current_user.pupil.id)):
        abort(403)

    session = db_session.create_session()

    pupil = session.query(Pupil).get(pupil_id)

    # Group.id, Topic.id, Group.name, Topic.name, func.count(distinct(Task.id)), solution_status
    tasks_success_count_of_pupil_for_topics = tasks_count_of_pupil_for_topic(pupil_id=pupil_id,
                                                                             solution_status=TaskCheckStatus.ACCESS)

    tasks_unsolved_count_of_pupil_for_topics = tasks_count_of_pupil_for_topic(pupil_id=pupil_id, solution_status=None)

    statistic_solved_and_unsolved_task_for_group_of_pupil = dict()

    for (group_id, topic_id), topic_statistic in groupby(
            tasks_success_count_of_pupil_for_topics + tasks_unsolved_count_of_pupil_for_topics, lambda x: (x[0], x[1])):

        topic_statistic = list(topic_statistic)

        group_name = topic_statistic[0][2]
        topic_name = topic_statistic[0][3]

        if len(topic_statistic) == 2:
            if topic_statistic[0][-1] is TaskCheckStatus.ACCESS:
                topic_solved_count, topic_unsolved_count = topic_statistic[0][4], topic_statistic[1][4]
            else:
                topic_unsolved_count, topic_solved_count = topic_statistic[1][4], topic_statistic[0][4]
        else:
            if topic_statistic[0][-1] is TaskCheckStatus.ACCESS:
                topic_solved_count, topic_unsolved_count = topic_statistic[0][4], 0
            else:
                topic_solved_count, topic_unsolved_count = 0, topic_statistic[0][4]

        topic_statistic_dict = {'topic_name': topic_name,
                                'solved': topic_solved_count,
                                'unsolved': topic_unsolved_count}

        if group_id not in statistic_solved_and_unsolved_task_for_group_of_pupil:
            statistic_solved_and_unsolved_task_for_group_of_pupil[group_id] = {'group_name': group_name,
                                                                               'topics': {
                                                                                   topic_id: topic_statistic_dict}}
        else:
            statistic_solved_and_unsolved_task_for_group_of_pupil[group_id]['topics'][topic_id] = topic_statistic_dict

    return render_template('pupil_profile.html', pupil=pupil,
                           statistic_for_group=statistic_solved_and_unsolved_task_for_group_of_pupil)


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


def blueprint_routes_register():
    app.register_blueprint(admin.blueprint, url_prefix="/admin")
    app.register_blueprint(teacher.blueprint, url_prefix='/teacher')
    app.register_blueprint(pupil.blueprint, url_prefix='/pupil')


def api_register():
    api.add_resource(PupilSolutionForTask, '/api_solution')
    api.add_resource(PupilSolutionsListForTask, '/api_solutions')


app.config.from_object(config_app.BaseConfig)
db_session.global_init(debug=app.config["DEBUG"])
add_default_admin()
blueprint_routes_register()
api_register()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"])
