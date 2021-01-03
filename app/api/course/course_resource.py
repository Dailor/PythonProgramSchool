from ...models import db_session
from app.models.course import Course
from app.models.teacher import Teacher

from .parser import parser_for_admin, parser_for_teacher

from flask import jsonify
from flask_restful import Resource, abort
from flask_login import current_user


def course_serializer(course):
    course_info = course.to_dict(only=('id', 'name', 'groups_id', 'curators_id', 'lessons_count'))
    return course_info


class CourseListResource(Resource):
    def get(self):
        session = db_session.create_session()
        courses = session.query(Course).all()
        return jsonify({'courses': [course_serializer(course) for course in courses]})

    def put(self):
        if current_user.is_admin:
            return self.put_handler_for_admin()
        elif current_user.is_teacher:
            return self.put_handler_for_teacher()

    def put_handler_for_admin(self):
        session = db_session.create_session()
        args = parser_for_admin.parse_args()
        teachers = session.query(Teacher).filter(Teacher.id.in_(args['curators_id'])).all()

        course = Course()
        course.name = args['name']
        course.curators = teachers

        session.add(course)
        session.commit()

        return jsonify(course_serializer(course))

    def put_handler_for_teacher(self):
        session = db_session.create_session()
        args = parser_for_teacher.parse_args()

        course = Course()
        course.name = args['name']
        course.curators = [current_user.teacher]

        session.add(course)
        session.commit()

        return jsonify(course_serializer(course))


class CourseResource(Resource):
    def get(self, course_id):
        course = Course.get_entity_or_404(course_id)

        return jsonify(course_serializer(course))

    def post(self, course_id):
        course = Course.get_entity_or_404(course_id)

        if current_user.is_admin:
            handler = self.post_handler_for_admin
        elif current_user.is_teacher:
            handler = self.post_handler_for_teacher

        return handler(course)

    def post_handler_for_admin(self, course):
        args = parser_for_admin.parse_args()

        session = db_session.create_session()

        teachers = session.query(Teacher).filter(Teacher.id.in_(args['curators_id'])).all()

        course.name = args['name']
        course.curators = teachers

        session.merge(course)
        session.commit()

        return jsonify(course_serializer(course))

    def post_handler_for_teacher(self, course):
        args = parser_for_teacher.parse_args()

        session = db_session.create_session()

        if not course.is_curator(current_user.teacher.id):
            return abort(403, error='Вы не можете изменять данный курс')

        course.name = args['name']
        course.curators = [current_user.teacher]

        session.merge(course)
        session.commit()

        return jsonify(course_serializer(course))

    def delete(self, course_id):

        session = db_session.create_session()

        course = Course.get_entity_or_404(course_id)

        if current_user.is_admin is False and current_user.teacher.id != course.teacher.id:
            return abort(403, error='Вы не можете удилать данный курс')

        session.delete(course)
        session.commit()

        return jsonify({'success': 'success'})
