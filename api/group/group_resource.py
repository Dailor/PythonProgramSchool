from models import db_session
from models.group import Group
from models.subject import Subject
from models.teacher import Teacher

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def check_group_by_id(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if group is None:
        abort(404, errro='Группа с {} ID не найдена'.format(group_id))


class GroupListResource(Resource):
    def get(self):
        session = db_session.create_session()

        groups = session.query(Group).all()

        return jsonify({'groups': [group.to_dict() for group in groups]})

    def put(self):
        args = parser.parse_args()
        session = db_session.create_session()

        subject = session.query(Subject).get(args['subject_id'])
        teacher = session.query(Teacher).get(args['teacher_id'])

        group_same_name = session.query(Group).filter(Group.name == args['name']).first()

        if not subject:
            abort(404, error="Предмета с таким ID нет")

        if not teacher:
            abort(404, error="Учителя с таким ID нет")

        if group_same_name is not None:
            abort(403, error="Группа с таким именем уже существует")

        group = Group()
        group.name = args['name']
        group.teacher = teacher
        group.is_active = args['is_active']

        if teacher not in subject.teachers:
            subject.teachers.append(teacher)

        subject.groups.append(group)

        session.merge(subject)
        session.commit()

        return jsonify(group.to_dict())


class GroupResource(Resource):
    def get(self, group_id):
        check_group_by_id(group_id)

        session = db_session.create_session()
        group = session.query(Group).get(group_id)

        return jsonify(group.to_dict(rules=('pupils', )))

    def post(self, group_id):
        check_group_by_id(group_id)

        args = parser.parse_args()
        session = db_session.create_session()

        subject = session.query(Subject).get(args['subject_id'])
        teacher = session.query(Teacher).get(args['teacher_id'])

        group_same_name = session.query(Group).filter(Group.name == args['name']).first()

        if not subject:
            abort(404, error="Предмета с таким ID нет")

        if not teacher:
            abort(404, error="Учителя с таким ID нет")

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

        session.merge(subject)
        session.commit()

        return jsonify(group.to_dict())

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
