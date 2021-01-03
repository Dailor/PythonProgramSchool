from flask import jsonify
from werkzeug.exceptions import Forbidden
from flask_restful import Resource, abort

from app.config_app import PaginationConfig, DefaultAdminConfig
from app.models import db_session
from app.models.user import FAKE_PASSWORD, User

from .parser import parser


def user_serializer(user):
    user_serialized = user.to_dict(only=('id', 'name', 'surname', 'email', 'confident_info', 'role_id'))
    user_serialized['password'] = FAKE_PASSWORD
    user_serialized['roles'] = user.get_string_role()
    return user_serialized


class UserListResource(Resource):
    def get(self):
        # args = parser_get_users.parse_args()

        session = db_session.create_session()

        query = session.query(User)

        # users = query.limit(args['limit']).offset(args['offset']).all()

        users = query.all()

        users_serialized = list()
        for user in users:
            users_serialized.append(user_serializer(user))

        return jsonify({'users': users_serialized})

    def put(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = session.query(User).filter(User.email == args['email']).first()
        if user:
            return abort(Forbidden.code, message="Пользователь с таким email'ом уже существует")

        user = User()

        user.name = args['name']
        user.surname = args['surname']
        user.email = args['email']
        user.confident_info = args['confident_info']
        user.set_password(args['password'])
        user.set_role(args['role_id'])

        session.add(user)
        session.commit()

        return jsonify(user_serializer(user))


class UserResource(Resource):
    def post(self, user_id):
        args = parser.parse_args()

        session = db_session.create_session()
        user = User.get_entity_or_404(user_id)

        user.name = args['name']
        user.surname = args['surname']
        user.email = args['email']
        user.confident_info = args['confident_info']
        user.set_role(args['role_id'])

        if FAKE_PASSWORD != args['password']:
            user.set_password(args['password'])

        session.merge(user)
        session.commit()

        return jsonify(user_serializer(user))

    def delete(self, user_id):
        session = db_session.create_session()
        user = User.get_entity_or_404(user_id)

        if user.id != DefaultAdminConfig.ADMIN_DEFAULT_ID:
            session.delete(user)
            session.commit()
        else:
            return abort(403)