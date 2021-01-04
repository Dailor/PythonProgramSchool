from app.models import db_session
from app.models.__all_models import Group, Teacher, Course

from .parser import parser, parser_admin

from flask import jsonify
from flask_restful import Resource, abort, request
from flask_login import current_user

groups_only_admin = ('id', 'name', 'is_active', 'teacher_id', 'courses_id')
groups_only_teacher = ('id', 'name', 'is_active', 'teacher_id', 'courses.id')


def get_groups_fields_to_serialize():
    if current_user.is_admin:
        return groups_only_admin
    elif current_user.is_teacher:
        return groups_only_teacher


class GroupListResource(Resource):
    def get(self):
        if not current_user.is_admin:
            return abort(403)

        session = db_session.create_session()

        groups = session.query(Group).all()

        return jsonify({'groups': [
            group.to_dict(only=groups_only_admin) for group in
            groups]})

    def put(self):
        if not (current_user.is_admin or current_user.is_teacher):
            return abort(403)

        args = parser_admin.parse_args()
        session = db_session.create_session()

        courses_id_list = args['courses_id']

        teacher = session.query(Teacher).get(args['teacher_id'])
        courses = session.query(Course).filter(Course.id.in_(courses_id_list)).all()

        group_same_name = session.query(Group).filter(Group.name == args['name']).first()

        if not teacher:
            return abort(404, error="Учителя с таким ID нет")

        if len(courses) != len(courses_id_list):
            id_course_have = [course.id for course in courses]
            id_missing = [course_id for course_id in courses_id_list if course_id not in id_course_have]
            return abort(404, error=f'Категории с {id_missing} нет')

        if group_same_name is not None:
            abort(403, error="Группа с таким именем уже существует")

        group = Group()
        group.name = args['name']
        group.generate_invite_code()
        group.teacher = teacher
        group.is_active = args['is_active']
        group.courses = courses

        session.add(group)
        session.commit()

        return jsonify(group.to_dict(only=get_groups_fields_to_serialize()))


class GroupResource(Resource):
    def get(self, group_id):
        group = Group.get_entity_or_404(group_id)
        group.is_have_permission(current_user)

        return jsonify(group.to_dict(rules=('pupils',)))

    def post(self, group_id):
        args = parser.parse_args()

        group = Group.get_entity_or_404(group_id)
        group.is_have_permission(current_user)

        courses_id = args['courses_id']

        session = db_session.create_session()

        if current_user.is_teacher:
            teacher = current_user.teacher
        elif current_user.is_admin:
            admin_args = parser_admin.parse_args()
            teacher = session.query(Teacher).get(admin_args['teacher_id'])

        courses = session.query(Course).filter(Course.id.in_(courses_id)).all()

        if len(courses) != len(courses_id):
            id_courses_have = [course.id for course in courses]
            id_missing = [course_id for course_id in courses_id if course_id not in id_courses_have]
            return abort(404, error=f'Категории с {id_missing} нет')

        group.name = args['name']
        group.is_active = args['is_active']
        group.teacher = teacher

        group.courses = courses

        session.merge(group)
        session.commit()

        return jsonify(group.to_dict(only=get_groups_fields_to_serialize()))

    def delete(self, group_id):
        session = db_session.create_session()

        group = Group.get_entity_or_404(group_id)
        group.is_have_permission(current_user)

        session.delete(group)
        session.commit()

        return jsonify({'success': 'success'})

    def patch(self, group_id):
        session = db_session.create_session()

        group = Group.get_entity_or_404(group_id)
        group.is_have_permission(current_user)

        group.generate_invite_code()

        session.merge(group)
        session.commit()

        return jsonify({'group': {'invite_code': group.invite_code}})
