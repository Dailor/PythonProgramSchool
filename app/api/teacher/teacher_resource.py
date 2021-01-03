from flask import jsonify
from flask_restful import Resource, abort
from app.models import db_session
from app.models.teacher import Teacher
from app.api.user.user_resource import user_serializer


def check_teacher_by_id(teacher_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    if teacher is None:
        abort(404, f'Учитель с {teacher_id} ID не найден')


def teacher_serializer(teacher):
    teacher_serialized = user_serializer(teacher.user)
    teacher_serialized['id'] = teacher.id
    teacher_serialized['groups'] = '\n'.join(teacher.get_string_groups())
    teacher_serialized['subjects'] = '\n'.join(teacher.get_string_subjects())
    return teacher_serialized


class TeacherListResource(Resource):
    def get(self):
        session = db_session.create_session()
        teachers = session.query(Teacher).all()

        teachers_to_users = [teacher_serializer(teacher) for teacher in teachers]

        return jsonify({"teachers": teachers_to_users})


class TeacherResource(Resource):
    def delete(self, teacher_id):
        check_teacher_by_id(teacher_id)

        session = db_session.create_session()
        teacher = session.query(Teacher).get(teacher_id)
        session.delete(teacher)
        session.commit()
        return jsonify({'success': 'success'})
