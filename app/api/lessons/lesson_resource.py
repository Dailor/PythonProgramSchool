from app.config_app import CheckerConfig

from ...models import db_session
from app.models.group import Group
from app.models.course import Course
from app.models.lesson import Lesson, LessonAvailableToGroup
from app.models.task import Task

from .parser import parser, parser_lesson_available, parser_lesson_available_contest

from flask import jsonify
from flask_restful import Resource, abort

from datetime import datetime


def lesson_serializer(lesson):
    return lesson.to_dict(only=('id', 'name'))


class LessonsListResource(Resource):
    def get(self, course_id):
        Course.get_entity_or_404(course_id)

        session = db_session.create_session()
        lessons = session.query(Lesson).filter(Lesson.course_id == course_id)

        return jsonify({'lessons': [lesson_serializer(lesson) for lesson in lessons]})

    def put(self, course_id):
        args = parser.parse_args()
        session = db_session.create_session()

        course = Course.get_entity_or_404(course_id)

        lesson = Lesson()
        lesson.name = args['name']
        lesson.html = args['html_page']

        for task_dict in args['tasks']:
            time_limit = task_dict['time_limit']
            memory_limit = task_dict['memory_limit']
            tries_limit = task_dict['tries_limit']
            language_id = args['language_id']

            if time_limit > CheckerConfig.CPU_TIME_LIMIT_MAX:
                abort(400, error=f"Не соблюден лимит по времени {CheckerConfig.CPU_TIME_LIMIT_MAX}")

            if memory_limit > CheckerConfig.MEMORY_LIMIT_MAX_MB:
                abort(400, error=f"Не соблюден лимит по памяти {CheckerConfig.MEMORY_LIMIT_MAX_MB}")

            task = Task()

            task.name = task_dict['name']
            task.description = task_dict['description']
            task.solutions = task_dict['solutions']
            task.examples = task_dict['examples']
            task.examples_hidden = task_dict['examples_hidden']
            task.api_check = task_dict['api_check']
            task.time_sec = time_limit
            task.memory_mb = memory_limit
            task.tries_count = tries_limit
            task.language_id = language_id

            lesson.tasks.append(task)

        course.lessons.append(lesson)

        session.merge(course)
        session.commit()

        return jsonify({'success': 'success'})


class LessonResource(Resource):
    def get(self, lesson_id):
        lesson = Lesson.get_entity_or_404(lesson_id)

        return jsonify(lesson_serializer(lesson))

    def post(self, course_id, lesson_id):
        Course.get_entity_or_404(course_id)
        lesson = Lesson.get_entity_or_404(lesson_id)

        args = parser.parse_args()
        session = db_session.create_session()

        lesson.tasks.clear()
        # for task in lesson.tasks:
        #     session.delete(task)

        lesson.name = args['name']
        lesson.html = args['html_page']

        for task_dict in args['tasks']:
            time_limit = task_dict['time_limit']
            memory_limit = task_dict['memory_limit']
            tries_limit = task_dict['tries_limit']
            language_id = args['language_id']

            if time_limit > CheckerConfig.CPU_TIME_LIMIT_MAX:
                abort(400, error=f"Не соблюден лимит по времени {CheckerConfig.CPU_TIME_LIMIT_MAX}")

            if memory_limit > CheckerConfig.MEMORY_LIMIT_MAX_MB:
                abort(400, error=f"Не соблюден лимит по памяти {CheckerConfig.MEMORY_LIMIT_MAX_MB}")

            task = Task()

            task.name = task_dict['name']
            task.description = task_dict['description']
            task.solutions = task_dict['solutions']
            task.examples = task_dict['examples']
            task.examples_hidden = task_dict['examples_hidden']
            task.api_check = task_dict['api_check']

            task.time_sec = time_limit
            task.memory_mb = memory_limit
            task.tries_count = tries_limit

            task.language_id = language_id

            lesson.tasks.append(task)

        session.merge(lesson)
        session.commit()

        return jsonify({'success': 'success'})

    def delete(self, course_id, lesson_id):
        Course.get_entity_or_404(course_id)
        lesson = Lesson.get_entity_or_404(lesson_id)

        session = db_session.create_session()

        session.delete(lesson)
        session.commit()

        return jsonify({'success': 'success'})


class LessonAvailableListResource(Resource):
    def put(self):
        args = parser_lesson_available.parse_args()

        group_id = args['group_id']
        lesson_id = args['lesson_id']

        session = db_session.create_session()

        lesson = Lesson.get_entity_or_404(lesson_id)
        group = Group.get_entity_or_404(group_id)

        if not (lesson.course in group.courses):
            return abort(403, error=f'Урок с {lesson_id} ID не находится в категориях данной группы')

        if lesson in group.lessons:
            return abort(403, error=f'Этот урок уже доступен этой группе')

        group.lessons.append(lesson)

        session.merge(group)
        session.commit()

        return jsonify({'success': 'success'})

    def delete(self):
        args = parser_lesson_available.parse_args()

        group_id = args['group_id']
        lesson_id = args['lesson_id']

        session = db_session.create_session()

        lesson = Lesson.get_entity_or_404(lesson_id)
        group = Group.get_entity_or_404(group_id)

        if not lesson in group.lessons:
            abort(404, error='Урок не был отрыт для этой группы')

        group.lessons.remove(lesson)
        session.merge(group)

        session.commit()

        return jsonify({'success': 'success'})

    def patch(self):
        args = parser_lesson_available_contest.parse_args()

        group_id = args['group_id']
        lesson_id = args['lesson_id']
        deadline = args['deadline']

        deadline_datetime = datetime.fromtimestamp(deadline)
        if deadline_datetime < datetime.utcnow():
            return abort(400, error='Дата должна быть позже чем сейчас')

        session = db_session.create_session()

        lesson = Lesson.get_entity_or_404(lesson_id)
        group = Group.get_entity_or_404(group_id)

        if lesson in group.lessons:
            return abort(403, error=f'Этот урок уже доступен этой группе')

        lesson_available_contest = LessonAvailableToGroup()
        lesson_available_contest.group_id = group_id
        lesson_available_contest.lesson_id = lesson_id
        lesson_available_contest.deadline = deadline_datetime

        session.add(lesson_available_contest)
        session.commit()

        return jsonify({'success': 'success'})
