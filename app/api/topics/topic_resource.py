from ...models import db_session
from app.models.topic import Topic
from app.models.teacher import Teacher
from app.models.group import Group

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def check_topic_by_id(topic_id):
    session = db_session.create_session()
    topic = session.query(Topic).get(topic_id)

    if topic is None:
        abort(404, error=f'Категория с {topic_id} ID не найдена')


def check_group(group, group_id):
    if group is None:
        abort(404, error=f'Группа с {group_id} ID не найдене')
    return group


class TopicListResource(Resource):
    def get(self):
        session = db_session.create_session()
        topics = session.query(Topic)
        return jsonify({'topics': [topic.to_dict() for topic in topics]})

    def put(self):
        session = db_session.create_session()
        args = parser.parse_args()

        teacher = session.query(Teacher).get(args['author_teacher_id'])
        if teacher is None:
            abort(404, error=f'Учитель с {args["author_teacher_id"]} не найден')

        topic = Topic()
        topic.name = args['name']
        topic.teacher = teacher
        topic.groups = [check_group(session.query(Group).get(group_id), group_id) for group_id in args['groups_id[]']]

        session.add(teacher)
        session.commit()

        return jsonify(topic.to_dict())


class TopicResource(Resource):
    def get(self, topic_id):
        check_topic_by_id(topic_id)

        session = db_session.create_session()
        topic = session.query(Topic).get(topic_id)

        return jsonify(topic.to_dict())

    def post(self, topic_id):
        check_topic_by_id(topic_id)
        args = parser.parse_args()

        session = db_session.create_session()
        topic = session.query(Topic).get(topic_id)

        teacher = session.query(Teacher).get(args['author_teacher_id'])
        if teacher is None:
            abort(404, error=f'Учитель с {args["author_teacher_id"]} не найден')

        topic.name = args['name']

        topic.name = args['name']
        topic.teacher = teacher
        topic.groups = [check_group(session.query(Group).get(group_id), group_id) for group_id in args['groups_id[]']]

        session.merge(teacher)
        session.commit()

        return jsonify(topic.to_dict())

    def delete(self, topic_id):
        check_topic_by_id(topic_id)
        session = db_session.create_session()

        topic = session.query(Topic).get(topic_id)

        session.delete(topic)
        session.commit()

        return jsonify({'success': 'success'})
