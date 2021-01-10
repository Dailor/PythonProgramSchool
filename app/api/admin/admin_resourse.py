from app.models import db_session
from app.models.__all_models import Admin, User, UserRoles
from app.api.user.user_resource import user_serializer

from flask import jsonify
from flask_restful import Resource


def admin_serializer(admin):
    admin_serialized = user_serializer(admin.user)

    return admin_serialized


class AdminListResource(Resource):
    def get(self):
        session = db_session.create_session()

        admins = session.query(Admin).all()

        return jsonify({'admins': [admin_serializer(admin) for admin in admins]})


class AdminResource(Resource):
    def delete(self, user_id):
        session = db_session.create_session()

        user = User.get_entity_or_404(user_id)
        user.set_role(UserRoles.WITHOUT_ROLE.value)

        session.commit()
