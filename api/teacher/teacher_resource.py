from flask import jsonify
from flask_restful import Resource, abort
from models import db_session
from models.teacher import Teacher
from api.user.user_resource import user_serializer


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


class TeacherDictIdToFullName(Resource):
    def get(self):
        session = db_session.create_session()
        teachers = session.query(Teacher)
        return jsonify({
            teacher.id: teacher.user.full_name for teacher in teachers
        })
