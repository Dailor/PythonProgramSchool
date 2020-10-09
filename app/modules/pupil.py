from app.models import db_session
from app.models.group import Group
from app.models.lesson import Lesson
from app.models.task import Task
from app.models.queries import count_tasks_solved_for_lessons_by_pupil, count_tasks_in_each_lesson_available_for_group

from app.api.task.task_resource import SolutionsListResource

from flask import render_template, abort, redirect
from flask.blueprints import Blueprint
from flask_login import current_user
from flask_restful import Api

blueprint = Blueprint('pupil', __name__, template_folder="templates", static_folder="static")
api = Api(blueprint)
api.add_resource(SolutionsListResource, '/api_solution')


def check_group_permission(group):
    pupil = current_user.pupil
    if not (group.id in pupil.groups_id):
        return abort(403)


@blueprint.before_request
def before_request_func():
    if not current_user.is_authenticated:
        return redirect("/login")


@blueprint.route('/groups/<int:group_id>')
def group_page(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)

    check_group_permission(group)

    pupil_id = current_user.pupil.id

    lessons_solve_status = dict(count_tasks_solved_for_lessons_by_pupil(pupil_id=pupil_id, group_id=group_id))
    count_tasks_in_lesson = dict(count_tasks_in_each_lesson_available_for_group(group_id=group_id))

    return render_template('lessons_available.html', group=group, lessons=group.lessons,
                           lessons_solve_status=lessons_solve_status, count_tasks_in_lesson=count_tasks_in_lesson)


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>')
def lesson_page(group_id, lesson_id):
    session = db_session.create_session()

    group = session.query(Group).get(group_id)
    check_group_permission(group)

    lesson = session.query(Lesson).get(lesson_id)
    if lesson not in group.lessons:
        abort(403)

    return render_template('lesson_page.html', lesson=lesson, group_id=group_id)


@blueprint.route('/groups/<int:group_id>/lesson/<int:lesson_id>/task/<int:task_id>')
def solve_task_page(group_id, lesson_id, task_id):
    session = db_session.create_session()

    group = session.query(Group).get(group_id)
    lesson = session.query(Lesson).get(lesson_id)
    task = session.query(Task).get(task_id)

    pupil_id = current_user.pupil.id

    check_group_permission(group)

    return render_template('solution_page.html', task=task, group_id=group_id, pupil_id=pupil_id)
