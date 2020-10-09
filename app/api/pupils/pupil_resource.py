from ...models import db_session
from app.models.pupil import Pupil
from app.models.group import Group

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def check_pupil_by_id(pupil_id):
    session = db_session.create_session()
    pupil = session.query(Pupil).get(pupil_id)
    if not pupil:
        abort(404, error="Ученик с {} ID не найден".format(pupil_id))


def check_group(group, group_id):
    if group is None:
        abort(404, error=f'Группа с {group_id} id не найдена')
    return group


class PupilListResource(Resource):
    def get(self):
        session = db_session.create_session()

        pupils = session.query(Pupil).all()

        return jsonify({"pupils": [pupil.to_dict() for pupil in pupils]})


class PupilResource(Resource):
    def post(self, pupil_id):
        check_pupil_by_id(pupil_id)

        args = parser.parse_args()
        session = db_session.create_session()

        pupil = session.query(Pupil).get(pupil_id)
        pupil.groups = [check_group(session.query(Group).get(group_id), group_id) for group_id in args['groups_id[]']]

        session.merge(pupil)
        session.commit()

        return jsonify(pupil.to_dict())

    def delete(self, pupil_id):
        check_pupil_by_id(pupil_id)

        session = db_session.create_session()
        pupil = session.query(Pupil).get(pupil_id)

        session.delete(pupil)
        session.commit()
        return jsonify({'success': 'success'})
