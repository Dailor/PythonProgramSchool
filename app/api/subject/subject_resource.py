from ...models import db_session
from app.models.subject import Subject

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def check_subject_by_id(subject_id):
    session = db_session.create_session()
    if session.query(Subject).get(subject_id) is None:
        abort(404, error=f"Предмет с {subject_id} ID не найден")


class SubjectListResource(Resource):
    def get(self):
        session = db_session.create_session()

        subjects = session.query(Subject).all()
        return jsonify({'subjects': [subject.to_dict() for subject in subjects]})

    def put(self):
        session = db_session.create_session()
        args = parser.parse_args()

        subject = Subject()
        subject.name = args['name']

        session.add(subject)
        session.commit()

        return jsonify(subject.to_dict())


class SubjectResource(Resource):
    def post(self, subject_id):
        check_subject_by_id(subject_id)

        session = db_session.create_session()
        args = parser.parse_args()

        subject = session.query(Subject).get(subject_id)
        subject.name = args['name']

        session.merge(subject)
        session.commit()

        return jsonify(subject.to_dict())

    def delete(self, subject_id):
        check_subject_by_id(subject_id)

        session = db_session.create_session()

        subject = session.query(Subject).get(subject_id)
        session.delete(subject)
        session.commit()

        return jsonify({'success': 'success'})


class SubjectDictIdToName(Resource):
    def get(self):
        return jsonify(self.subjects_dict())

    def subjects_dict(self):
        session = db_session.create_session()
        subjects = session.query(Subject)
        return {
            subject.id: subject.name for subject in subjects
        }
