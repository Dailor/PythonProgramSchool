from api.topics.topic_resource import check_topic_by_id
from api.group.group_resource import check_group_by_id

from models import db_session
from models.group import Group
from models.topic import Topic
from models.lesson import Lesson
from models.task import Task, TaskCheckMethods

from .parser import parser, parser_lesson_available

from flask import jsonify, request
from flask_restful import Resource, abort


def check_lesson_by_id(lesson_id):
    session = db_session.create_session()
    lesson = session.query(Lesson).get(lesson_id)

    if lesson is None:
        abort(404, error=f'Урок с {lesson_id} не найден')


class LessonsListResource(Resource):
    def get(self, topic_id):
        check_topic_by_id(topic_id)

        session = db_session.create_session()
        lessons = session.query(Lesson).filter(Lesson.topic_id == topic_id)

        return jsonify({'lessons': [lesson.to_dict() for lesson in lessons]})

    def put(self, topic_id):
        check_topic_by_id(topic_id)

        args = parser.parse_args()
        session = db_session.create_session()

        topic = session.query(Topic).get(topic_id)

        lesson = Lesson()
        lesson.name = args['name']
        lesson.html = args['html_page']

        for task_dict in args['tasks']:
            task = Task()

            task.name = task_dict['name']
            task.description = task_dict['description']
            task.in_data = task_dict['in_data']
            task.out_data = task_dict['out_data']
            task.type_check = TaskCheckMethods.MANUAL_CHECK

            lesson.tasks.append(task)

        topic.lessons.append(lesson)

        session.merge(topic)
        session.commit()

        return jsonify({'success': 'success'})


class LessonResource(Resource):
    def get(self, lesson_id):
        check_lesson_by_id(lesson_id)

        session = db_session.create_session()

        lesson = session.query(Lesson).get(lesson_id)

        return jsonify(lesson.to_dict())

    def post(self, topic_id, lesson_id):
        check_topic_by_id(topic_id)
        check_lesson_by_id(lesson_id)

        args = parser.parse_args()
        session = db_session.create_session()

        lesson = session.query(Lesson).get(lesson_id)
        lesson.tasks = []

        lesson.name = args['name']
        lesson.html = args['html_page']

        for task_dict in args['tasks']:
            task = Task()

            task.name = task_dict['name']
            task.description = task_dict['description']
            task.in_data = task_dict['in_data']
            task.out_data = task_dict['out_data']
            task.type_check = TaskCheckMethods.MANUAL_CHECK

            lesson.tasks.append(task)

        session.merge(lesson)
        session.commit()

        return jsonify({'success': 'success'})

    def delete(self, topic_id, lesson_id):
        check_topic_by_id(topic_id)
        check_lesson_by_id(lesson_id)

        session = db_session.create_session()
        lesson = session.query(Lesson).get(lesson_id)

        session.delete(lesson)
        session.commit()

        return jsonify({'success': 'success'})


class LessonAvailableListResource(Resource):
    def put(self):
        args = parser_lesson_available.parse_args()

        group_id = args['group_id']
        lesson_id = args['lesson_id']

        check_group_by_id(group_id)
        check_lesson_by_id(lesson_id)

        session = db_session.create_session()

        lesson = session.query(Lesson).get(lesson_id)
        group = session.query(Group).get(group_id)

        if not (lesson.topic in group.topics):
            abort(403, error=f'Урок с {lesson_id} ID не находится в категориях данной группы')

        if lesson in group.lessons:
            abort(403, error=f'Этот урок уже доступен этой группе')

        group.lessons.append(lesson)
        session.merge(group)

        session.commit()

        return jsonify({'success': 'success'})

    def delete(self):
        args = parser_lesson_available.parse_args()

        group_id = args['group_id']
        lesson_id = args['lesson_id']

        check_group_by_id(group_id)
        check_lesson_by_id(lesson_id)

        session = db_session.create_session()

        lesson = session.query(Lesson).get(lesson_id)
        group = session.query(Group).get(group_id)

        if not lesson in group.lessons:
            abort(404, error='Урок не был отрыт для этой группы')

        group.lessons.remove(lesson)
        session.merge(group)

        session.commit()

        return jsonify({'success': 'success'})
