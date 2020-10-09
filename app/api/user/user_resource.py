from flask import jsonify, request
from werkzeug.exceptions import Forbidden, BadRequest
from flask_restful import Resource, abort

from ...models import db_session
from app.models.user import UserRoles, FAKE_PASSWORD, Admin, User
from app.models.teacher import Teacher
from app.models.pupil import Pupil

from .parser import parser, parser_role


def user_serializer(user):
    user_serialized = user.to_dict()
    user_serialized['password'] = FAKE_PASSWORD
    user_serialized['roles'] = user.get_string_role()
    return user_serialized


def check_user_by_id(user_id):
    session = db_session.create_session()
    if session.query(User).get(user_id) is None:
        abort(404, error=f"Пользователь с {user_id} ID не найден")


class UserListResource(Resource):
    def get(self):
        role = request.args.get("role", "").lower()
        session = db_session.create_session()

        role_in_query = None

        if role == UserRoles.ADMIN:
            role_in_query = Admin
        elif role == UserRoles.TEACHER:
            role_in_query = Teacher
        elif role == UserRoles.PUPIL:
            role_in_query = Pupil

        if role_in_query is None:
            users = session.query(User)
        else:
            users = session.query(User).join(role_in_query)

        users_serialized = list()
        for user in users:
            users_serialized.append(user_serializer(user))

        return jsonify({'users': users_serialized})

    def put(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = session.query(User).filter(User.email == args['email']).first()
        if user:
            abort(Forbidden.code, error="Пользователь с таким email'ом уже существует")

        user = User()
        user.name = args['name']
        user.surname = args['surname']
        user.email = args['email']
        user.confident_info = args['confident_info']
        user.set_password(args['password'])

        session.add(user)
        session.commit()

        return jsonify(user_serializer(user))


class UserResource(Resource):
    def post(self, user_id):
        check_user_by_id(user_id)

        args = parser.parse_args()

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        user_check_email = session.query(User).filter(User.email == args['email']).first()

        if user_check_email and user_check_email.id != user.id:
            abort(Forbidden.code, error="Пользователь с таким email'ом уже существует")

        user.name = args['name']
        user.surname = args['surname']
        user.email = args['email']
        user.confident_info = args['confident_info']

        if FAKE_PASSWORD != args['password']:
            user.set_password(args['password'])

        session.merge(user)
        session.commit()

        return jsonify(user_serializer(user))


class RoleSetterResource(Resource):
    def post(self):
        args = parser_role.parse_args()
        check_user_by_id(args['id'])
        session = db_session.create_session()

        role_string = args["role"].lower()

        if role_string not in UserRoles.ALL_ROLES:
            return abort(BadRequest.code, error="Такой роли нет")

        user = session.query(User).get(args['id'])

        if user.is_have_role:
            return abort(Forbidden.code,
                         error=f"Пользователь уже имеет роль '{user.get_string_role}',"
                               f" чтобы удалить роль войдите в раздел для этой роли")

        if role_string == UserRoles.ADMIN:
            role = Admin()
        elif role_string == UserRoles.TEACHER:
            role = Teacher()
        elif role_string == UserRoles.PUPIL:
            role = Pupil()

        role.user = user
        session.add(role)
        session.commit()

        return jsonify(user_serializer(user))

    def delete(self):
        args = parser_role.parse_args()
        check_user_by_id(args['id'])
        session = db_session.create_session()

        role_string = args["role"].lower()

        if role_string not in UserRoles.ALL_ROLES:
            return abort(BadRequest.code, error="Такой роли нет")

        if role_string not in UserRoles.ALL_ROLES:
            return abort(BadRequest.code, error="Такой роли нет")

        user = session.query(User).get(args['id'])

        if role_string == UserRoles.ADMIN:
            if user.id == 1:
                abort(Forbidden.code, error='Нельзя удалить роль Админ у пользователя с первым ID')
            session.delete(user.admin)

        session.commit()
        return jsonify(user_serializer(user))
