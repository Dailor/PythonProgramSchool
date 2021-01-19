from app.config_app import CheckerConfig

from app.models import db_session
from app.models.__all_models import Group, Course, Lesson, Pupil, Task, ProgrammingLanguage

from app.models.queries import count_tasks_solved_for_lessons_by_pupils_in_group, \
    count_tasks_in_each_lesson_available_for_group

from app.api.group.group_resource import GroupResource
from app.api.lessons.lesson_resource import LessonsListResource, LessonResource, LessonAvailableListResource
from app.api.task.task_resource import SolutionsListResource
from app.api.course.course_resource import CourseListResource, CourseResource

from flask import render_template, redirect, abort
from flask.blueprints import Blueprint
from flask_login import current_user
from flask_restful import Api

blueprint = Blueprint('teacher', __name__, template_folder="templates", static_folder="static")
api = Api(blueprint, prefix='/api')


def register_resources():
    api.add_resource(GroupResource, '/group/<int:group_id>')

    api.add_resource(LessonsListResource, '/course/<int:course_id>/lesson')
    api.add_resource(LessonResource, '/course/<int:course_id>/lesson/<int:lesson_id>')
    api.add_resource(LessonAvailableListResource, '/lesson_available')

    api.add_resource(SolutionsListResource, '/solutions/group/<int:group_id>/task/<int:task_id>')

    api.add_resource(CourseResource, '/course/<int:course_id>')
    api.add_resource(CourseListResource, '/course')


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

    return render_template('/teacher/group.html', group=group)


@blueprint.route('/course/<int:course_id>')
def course_page(course_id):
    course = Course.get_entity_or_404(course_id)

    if not course.is_curator(current_user.teacher):
        return abort(403)

    return render_template('/teacher/lessons_in_course.html', course=course)


@blueprint.route('/course/<int:course_id>/lesson')
def lesson_add_page(course_id):
    course = Course.get_entity_or_404(course_id)

    http_request_type = 'PUT'
    page_type = 'Добавить'

    return render_template('/teacher/lesson_edit.html',
                           course=course,
                           http_request_type=http_request_type,
                           page_type=page_type,
                           ProgrammingLanguage=ProgrammingLanguage,
                           time_limit_max=CheckerConfig.CPU_TIME_LIMIT_MAX,
                           memory_limit_max=CheckerConfig.MEMORY_LIMIT_MAX_MB)


@blueprint.route('/course/<int:course_id>/lesson/<int:lesson_id>')
def lesson_edit_page(course_id, lesson_id):
    course = Course.get_entity_or_404(course_id)
    lesson = Lesson.get_entity_or_404(lesson_id)

    http_request_type = 'POST'
    page_type = 'Изменить'

    return render_template('/teacher/lesson_edit.html',
                           course=course,
                           lesson=lesson.to_dict(only=('id', 'name', 'html', 'tasks', '-tasks.lesson')),
                           http_request_type=http_request_type,
                           page_type=page_type,
                           ProgrammingLanguage=ProgrammingLanguage,
                           time_limit_max=CheckerConfig.CPU_TIME_LIMIT_MAX,
                           memory_limit_max=CheckerConfig.MEMORY_LIMIT_MAX_MB)


@blueprint.route('/groups/<int:group_id>/lessons')
def group_lessons_page(group_id):
    group = Group.get_entity_or_404(group_id)

    lessons = [lesson for course in group.courses for lesson in course.lessons]

    pupil_count_in_group = len(group.pupils)

    # [(lesson_id, task_id, count_pupils)]
    count_task_solved_for_lessons = count_tasks_solved_for_lessons_by_pupils_in_group(group_id=group_id)
    count_task_from_lessons_available_for_group = dict(
        count_tasks_in_each_lesson_available_for_group(group_id=group_id))

    progress_solved_tasks_by_pupils = dict()

    for lesson in lessons:
        task_solved = 0

        while len(count_task_solved_for_lessons) and count_task_solved_for_lessons[0][0] == lesson.id:
            if count_task_solved_for_lessons[0][2] == pupil_count_in_group:
                task_solved += 1
            del count_task_solved_for_lessons[0]

        progress_solved_tasks_by_pupils[lesson.id] = task_solved, count_task_from_lessons_available_for_group.get(
            lesson.id, 1)

    return render_template('lessons_for_group.html', group=group,
                           progress_solved_tasks_by_pupils=progress_solved_tasks_by_pupils)


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>')
def lesson_page(group_id, lesson_id):
    group = Group.get_entity_or_404(group_id)
    lesson = Lesson.get_entity_or_404(lesson_id)

    lesson_available = group.get_lesson_available_by_lesson(lesson, group)

    lesson_to_dict_only = (
        'id', 'name', 'tasks.id', 'tasks.name', 'html', 'tasks.description', 'tasks.time_sec', 'tasks.memory_mb',
        'tasks.examples')

    return render_template('lesson_page.html', group_id=group.id, lesson=lesson.to_dict(only=lesson_to_dict_only),
                           lesson_available=lesson_available)


@blueprint.route('/groups/<int:group_id>/lessons/<int:lesson_id>/task/<int:task_id>/pupil/<int:pupil_id>')
def solution_page(group_id, lesson_id, task_id, pupil_id):
    pupil = Pupil.get_entity_or_404(pupil_id)
    task = Task.get_entity_or_404(task_id)
    group = Group.get_entity_or_404(group_id)
    lesson = Lesson.get_entity_or_404(lesson_id)

    lesson_available = group.get_lesson_available_by_lesson(lesson, group)
    return render_template('solution_page.html', task=task, group_id=group_id,
                           pupil_id=pupil_id, pupil_full_name=pupil.user.full_name, lesson_available=lesson_available)


@blueprint.route('/groups')
def groups_page():
    current_teacher = current_user.teacher

    session = db_session.create_session()

    groups = {group.id: group.to_dict(
        only=('id', 'name', 'pupils.id', 'pupils.user.full_name', 'is_active', 'courses.id')) for group
        in current_teacher.groups}
    courses = {course.id: course.name for course in session.query(Course).all()}

    return render_template('/teacher/groups.html', groups=groups, courses=courses)


@blueprint.route('/lesson_view/<int:lesson_id>')
def lesson_page_view(lesson_id):
    session = db_session.create_session()

    lesson = session.query(Lesson).get(lesson_id)

    if lesson is None:
        abort(404)

    lesson_to_dict_only = (
        'id', 'name', 'tasks.id', 'tasks.name', 'html', 'tasks.description', 'tasks.time_sec', 'tasks.memory_mb',
        'tasks.examples')

    return render_template('lesson_page.html',
                           lesson_test_view=True,
                           lesson=lesson.to_dict(only=lesson_to_dict_only),
                           group_id=None)

register_resources()