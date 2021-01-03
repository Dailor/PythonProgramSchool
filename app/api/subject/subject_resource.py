from ...models import db_session
from app.models.subject import Subject

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort


def subject_serializer(subject):
    return subject.to_dict(only=('id', 'name', 'groups.name', 'teachers.name'))


class SubjectListResource(Resource):
    def get(self):
        session = db_session.create_session()

        subjects = session.query(Subject).all()
        return jsonify({'subjects': [subject_serializer(subject) for subject in subjects]})

    def put(self):
        session = db_session.create_session()
        args = parser.parse_args()

        subject = Subject()
        subject.name = args['name'].strip()

        session.add(subject)
        session.commit()

        return jsonify(subject_serializer(subject))


class SubjectResource(Resource):
    def post(self, subject_id):
        session = db_session.create_session()
        args = parser.parse_args()

        subject = Subject.get_entity_or_404(subject_id)
        subject.name = args['name'].strip()

        session.merge(subject)
        session.commit()

        return jsonify(subject_serializer(subject))

    def delete(self, subject_id):
        session = db_session.create_session()

        subject = Subject.get_entity_or_404(subject_id)
        session.delete(subject)
        session.commit()

        return jsonify({'success': 'success'})
