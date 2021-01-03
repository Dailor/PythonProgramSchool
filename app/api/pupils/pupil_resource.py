from ...models import db_session
from app.models.pupil import Pupil
from app.models.group import Group

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def pupil_serializer(pupil):
    return pupil.to_dict(only=('id', 'user.full_name', 'user.confident_info', 'groups_id',))


class PupilListResource(Resource):
    def get(self):
        session = db_session.create_session()

        pupils = session.query(Pupil).all()

        return jsonify({"pupils": [pupil_serializer(pupil) for pupil in pupils]})


class PupilResource(Resource):
    def post(self, pupil_id):
        args = parser.parse_args()
        session = db_session.create_session()

        pupil = Pupil.get_entity_or_404(pupil_id)
        pupil.groups = session.query(Group).filter(Group.id.in_(args['groups_id[]'])).all()
        pupil_groups_id = [group.id for group in pupil.groups]

        if len(pupil_groups_id) and  not any(group_id in pupil_groups_id for group_id in args['groups_id[]']) :
            return abort(404, error='Вы пытаетесь добавить ученика в группу которой нет')

        session.merge(pupil)
        session.commit()

        return jsonify(pupil_serializer(pupil))

    def delete(self, pupil_id):
        session = db_session.create_session()
        pupil = Pupil.get_entity_or_404(pupil_id)

        session.delete(pupil)
        session.commit()
        return jsonify({'success': 'success'})
