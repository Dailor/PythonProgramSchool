from app import app, recaptcha
from app.models import db_session
from app.models.group import Group
from app.models.pupil import Pupil
from app.models.task import TaskCheckStatus
from app.models.user import User
from app.models.queries import tasks_count_of_pupil_for_topic, groups_by_subject

from app.forms.login import LoginForm, LoginAnswers
from app.forms.registration import RegistrationForm
from app.forms.password_reset import ResetPasswordRequestForm, ResetPasswordForm

from app.utils import send_password_reset_email

from flask import render_template, redirect, abort, flash, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from itertools import groupby


def redirect_if_authed(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/index")
        return func(*args, **kwargs)

    return wrapper


@redirect_if_authed
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    captcha_error = False
    if form.is_submitted():
        if recaptcha.verify():
            session = db_session.create_session()
            user = session.query(User).filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
                flash('Вам на почту отправлены дальнейшие инструкции по восстановлению пароля.')
                return redirect(url_for('login'))
            else:
                flash("Пользователя с такой почтой нет!")
        else:
            captcha_error = True
    return render_template('reset_password_request.html', captcha_error=captcha_error, form=form)


@redirect_if_authed
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        session = db_session.create_session()
        session.merge(user)
        session.commit()
        flash('Ваш пароль успешно изменен')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@redirect_if_authed
@app.route("/login", methods=["GET", "POST"])
def login():
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


@redirect_if_authed
@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    captcha_error = False

    groups_by_subject_data = groups_by_subject()

    groups_by_subject_dict = dict()
    for group_id, group_name, subject_id, subject_name in groups_by_subject_data:
        group_info = {"id": group_id,
                      "name": group_name}

        if subject_id not in groups_by_subject_dict:
            groups_by_subject_dict[subject_id] = {"name": subject_name,
                                                  "groups": [group_info]}
        else:
            groups_by_subject_dict[subject_id]["groups"].append(group_info)

    if form.is_submitted():
        if recaptcha.verify():
            user = form.check_form()
            if user:
                session = db_session.create_session()
                group_ids = [int(x) for x in form.groups.data]
                groups = session.query(Group).filter(Group.id.in_(group_ids))
                pupil = Pupil()
                pupil.groups.extend(groups)

                user.pupil = pupil

                session.add(user)
                session.commit()
                flash("Аккаунт создан!")
                return redirect('/login')
        else:
            captcha_error = True

    form.subjects.choices = [
        (subject_id, groups_by_subject_dict[subject_id]['name']) for subject_id in groups_by_subject_dict]

    return render_template('registration.html', groups_by_subject_dict=groups_by_subject_dict, form=form,
                           captcha_error=captcha_error)


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

