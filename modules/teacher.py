from models import db_session
from models.queries.queries import tasks_count_of_pupils_for_topic
from models.group import Group
from models.topic import Topic
from models.lesson import Lesson
from models.task import Solutions, TaskCheckStatus

from api.group.group_resource import GroupResource, check_group_by_id
from api.lessons.lesson_resource import LessonsListResource, LessonResource, LessonAvailableListResource, \
    check_topic_by_id, check_lesson_by_id
from api.task.task_resource import SolutionsListResource

from flask import render_template, redirect, abort
from flask.blueprints import Blueprint
from flask_login import current_user
from flask_restful import Api

blueprint = Blueprint('teacher', __name__, template_folder="templates", static_folder="static")
api = Api(blueprint)

api.add_resource(GroupResource, '/api_group/<int:group_id>')
api.add_resource(LessonsListResource, '/api_lesson/<int:topic_id>')
api.add_resource(LessonResource, '/api_lesson/<int:topic_id>/lesson/<int:lesson_id>')
api.add_resource(LessonAvailableListResource, '/lesson_available_api')
api.add_resource(SolutionsListResource, '/api_solutions/group/<int:group_id>/task/<int:task_id>')


@blueprint.before_request
def before_request_func():
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.is_pupil:
        return abort(403)


@blueprint.route('/groups/<int:group_id>')
def group_page(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)

    if group is None:
        abort(404)

    if current_user.teacher.id != group.teacher_id:
        abort(403)

    return render_template('/teacher/group.html', group_id=group.id, group_name=group.name)


@blueprint.route('/topics/<int:topic_id>')
def topic_page(topic_id):
    session = db_session.create_session()
    topic = session.query(Topic).get(topic_id)

    check_topic_by_id(topic_id)

    if current_user.teacher.id != topic.author_teacher_id:
        abort(403)

    return render_template('/teacher/lessons_in_topic.html', topic_name=topic.name, topic_id=topic.id)


@blueprint.route('/topics/<int:topic_id>/lesson')
def lesson_add_page(topic_id):
    check_topic_by_id(topic_id)

    session = db_session.create_session()
    topic = session.query(Topic).get(topic_id)

    http_request_type = 'PUT'
    page_type = 'Добавить'

    return render_template('/teacher/lesson_edit.html', topic_id=topic.id, http_request_type=http_request_type,
                           page_type=page_type)


@blueprint.route('/topics/<int:topic_id>/lesson/<int:lesson_id>')
def lesson_edit_page(topic_id, lesson_id):
    check_topic_by_id(topic_id)
    check_lesson_by_id(lesson_id)

    session = db_session.create_session()
    topic = session.query(Topic).get(topic_id)
    lesson = session.query(Lesson).get(lesson_id)

    http_request_type = 'POST'
    page_type = 'Изменить'

    return render_template('/teacher/lesson_edit.html', topic_id=topic.id, http_request_type=http_request_type,
                           lesson=lesson.to_dict(),
                           page_type=page_type)


@blueprint.route('/groups/<int:group_id>/lessons')
def group_lessons_page(group_id):
    check_group_by_id(group_id)

    session = db_session.create_session()
    group = session.query(Group).get(group_id)

    lessons = [lesson for topic in group.topics for lesson in topic.lessons]
    return render_template('lessons_available.html', group=group, lessons=lessons)


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>')
def lesson_page(group_id, lesson_id):
    check_group_by_id(group_id)
    check_lesson_by_id(lesson_id)

    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    lesson = session.query(Lesson).get(lesson_id)

    is_lesson_available = lesson in group.lessons

    return render_template('lesson_page.html', group_id=group.id, lesson=lesson,
                           is_lesson_available=is_lesson_available)


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>/solution/<int:solution_id>')
def solution_page(group_id, lesson_id, solution_id):
    session = db_session.create_session()
    solution = session.query(Solutions).get(solution_id)
    return render_template('solution_page.html', solution=solution, task=solution.task, group_id=group_id)


def set_solution_status(solution_id, status):
    session = db_session.create_session()
    solution = session.query(Solutions).get(solution_id)
    solution.review_status = status
    session.merge(solution)
    session.commit()


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>/solution/<int:solution_id>/accept')
def accept_solution(group_id, lesson_id, solution_id):
    set_solution_status(solution_id, TaskCheckStatus.ACCESS)
    return redirect(f'/teacher/groups/{group_id}/lessons/{lesson_id}')


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>/solution/<int:solution_id>/decline')
def decline_solution(group_id, lesson_id, solution_id):
    set_solution_status(solution_id, TaskCheckStatus.FAILED)
    return redirect(f'/teacher/groups/{group_id}/lessons/{lesson_id}')


@blueprint.route('/groups')
def groups_page():
    current_teacher = current_user.teacher
    groups = {group.id: group.to_dict(rules=('pupils', )) for group in current_teacher.groups}
    return render_template('/teacher/groups.html', groups=groups)
