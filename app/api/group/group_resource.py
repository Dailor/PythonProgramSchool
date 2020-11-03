from app.models import db_session
from app.models.__all_models import Group, Subject, Teacher, Topic

from .parser import parser_admin, parser_teacher

from flask import jsonify, request
from flask_restful import Resource, abort
from flask_login import current_user

groups_only_admin = ('id', 'name', 'is_active', 'subject_id', 'teacher_id', 'topics.id', 'topics_id_list')


def check_group_by_id(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if group is None:
        abort(404, errro='Группа с {} ID не найдена'.format(group_id))


class GroupListResource(Resource):
    def get(self):
        session = db_session.create_session()

        groups = session.query(Group).all()

        return jsonify({'groups': [
            group.to_dict(only=groups_only_admin) for group in
            groups]})

    def put(self):
        args = parser_admin.parse_args()
        session = db_session.create_session()

        subject = session.query(Subject).get(args['subject_id'])
        teacher = session.query(Teacher).get(args['teacher_id'])
        topics = session.query(Topic).filter(Topic.id.in_(args['topics_id_list'])).all()

        group_same_name = session.query(Group).filter(Group.name == args['name']).first()

        if not subject:
            abort(404, error="Предмета с таким ID нет")

        if not teacher:
            abort(404, error="Учителя с таким ID нет")

        if len(topics) != len(args['topics_id_list']):
            id_topics_have = [topic.id for topic in topics]
            id_missing = [topic_id for topic_id in args['topics_id_list'] if topic_id not in id_topics_have]
            abort(404, error=f'Категории с {id_missing} нет')

        if group_same_name is not None:
            abort(403, error="Группа с таким именем уже существует")

        group = Group()
        group.name = args['name']
        group.teacher = teacher
        group.is_active = args['is_active']
        group.topics = topics

        if teacher not in subject.teachers:
            subject.teachers.append(teacher)

        subject.groups.append(group)

        session.add(group)
        session.merge(subject)
        session.commit()

        return jsonify(group.to_dict(only=groups_only_admin))


class GroupResource(Resource):
    def get(self, group_id):
        check_group_by_id(group_id)

        session = db_session.create_session()
        group = session.query(Group).get(group_id)

        return jsonify(group.to_dict(rules=('pupils',)))

    def post(self, group_id):
        check_group_by_id(group_id)

        session = db_session.create_session()

        if current_user.is_admin:
            args = parser_admin.parse_args()
            teacher = session.query(Teacher).get(args['teacher_id'])
        elif current_user.is_teacher:
            args = parser_teacher.parse_args()
            teacher = current_user.teacher

        subject = session.query(Subject).get(args['subject_id'])

        topics = session.query(Topic).filter(Topic.id.in_(args['topics_id_list'])).all()

        group_same_name = session.query(Group).filter(Group.name == args['name']).first()

        if not subject:
            abort(404, error="Предмета с таким ID нет")

        if not teacher:
            abort(404, error="Учителя с таким ID нет")

        if len(topics) != len(args['topics_id_list']):
            id_topics_have = [topic.id for topic in topics]
            id_missing = [topic_id for topic_id in args['topics_id_list'] if topic_id not in id_topics_have]
            abort(404, error=f'Категории с {id_missing} нет')

        group = session.query(Group).get(group_id)

        if group_same_name is not None and group_same_name.id != group.id:
            abort(403, error="Группа с таким именем уже существует")

        group.name = args['name']
        group.is_active = args['is_active']
        group.teacher = teacher

        if teacher not in subject.teachers:
            subject.teachers.append(teacher)

        if group not in subject.groups:
            subject.groups.append(group)

        group.topics = topics

        session.merge(subject)
        session.commit()

        return jsonify(group.to_dict(only=groups_only_admin))

    def post_handler_for_teacher(self):
        pass

    def delete(self, group_id):
        check_group_by_id(group_id)

        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        session.delete(group)
        session.commit()
        return jsonify({'success': 'success'})


class GroupsToDict(Resource):
    def get(self):
        return jsonify(self.get_groups_dict())

    def get_groups_dict(self):
        session = db_session.create_session()

        groups = dict()
        for group in session.query(Group).all():
            groups[group.id] = group.name
        return groups
