import config_app
from models import db_session
from models.group import Group
from models.lesson import Lesson
from models.pupil import Pupil
from models.task import Task, Solutions, TaskCheckStatus
from models.topic import Topic

from modules import admin, teacher, pupil

from models.user import User, Admin, UserRoles
from forms.login import LoginForm, LoginAnswers
from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_login.login_manager import LoginManager

from sqlalchemy import func, distinct, and_

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


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
    return render_template("index.html")


def tasks_count_of_pupils_for_topic(session, group_id, pupil_id, solution_status):
    query = session.query(Topic.id, Topic.name, func.count(distinct(Task.id))).select_from(Group)
    query = query.join(Group.topics)
    query = query.join(Lesson, Lesson.topic_id == Topic.id)
    query = query.join(Task, Task.lesson_id == Lesson.id)
    query = query.outerjoin(Solutions,
                            and_(Solutions.task_id == Task.id,
                                 Solutions.pupil_id == pupil_id,
                                 Solutions.group_id == group_id))
    if solution_status is TaskCheckStatus.ACCESS:
        query = query.filter(Solutions.review_status.is_(TaskCheckStatus.ACCESS))
    else:
        query = query.filter(Solutions.review_status.isnot(TaskCheckStatus.ACCESS))
    query = query.group_by(Topic.name, Topic.id)
    return query.all()


@app.route('/groups/<int:group_id>/pupils/<int:pupil_id>')
def pupil_profile(group_id, pupil_id):
    session = db_session.create_session()

    pupil = session.query(Pupil).get(pupil_id)

    tasks_success_count_of_pupil_for_topics = tasks_count_of_pupils_for_topic(session, group_id, pupil_id,
                                                                              TaskCheckStatus.ACCESS)

    tasks_unsolved_count_of_pupil_for_topics = tasks_count_of_pupils_for_topic(session, group_id, pupil_id, None)

    statistic_solved_and_unsolved_task_by_pupil_for_group = dict()

    for topic_id, topic_name, tasks_count in tasks_success_count_of_pupil_for_topics:
        statistic_solved_and_unsolved_task_by_pupil_for_group[topic_id] = {'topic_name': topic_name,
                                                                           'solved': tasks_count,
                                                                           'unsolved': 0}

    for topic_id, topic_name, tasks_count in tasks_unsolved_count_of_pupil_for_topics:
        statistic_for_topic = statistic_solved_and_unsolved_task_by_pupil_for_group.get(topic_id,
                                                                                        {'topic_name': topic_name,
                                                                                         'solved': 0})
        statistic_for_topic['unsolved'] = tasks_count

        statistic_solved_and_unsolved_task_by_pupil_for_group[topic_id] = statistic_for_topic

    return render_template('pupil_profile.html', pupil=pupil,
                           statistic_for_topics=statistic_solved_and_unsolved_task_by_pupil_for_group)



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


def blueprint_routes():
    app.register_blueprint(admin.blueprint, url_prefix="/admin")
    app.register_blueprint(teacher.blueprint, url_prefix='/teacher')
    app.register_blueprint(pupil.blueprint, url_prefix='/pupil')


if __name__ == '__main__':
    app.config.from_object(config_app.DevelopmentConfig)
    db_session.global_init(debug=app.config["DEBUG"])
    add_default_admin()
    blueprint_routes()
    app.run(host=app.config["HOST"], port=app.config["PORT"])
