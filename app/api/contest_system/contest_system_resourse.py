from .parser import parser_change

from app.models.db_session import create_session
from app.models.__all_models import ContestSystem, ContestSystemToPupil, Pupil

from flask_restful import Resource


class ContestSystemPupilListResource(Resource):
    def get(self, pupil_id):
        pupil = Pupil.get_entity_or_404(pupil_id)
        contest_systems_pupil = pupil.contest_systems
        return {contest_system_pupil.contest_system_id: contest_system_pupil.id_on_contest_system
                for contest_system_pupil in contest_systems_pupil}


class ContestSystemPupilResource(Resource):
    def post(self, pupil_id, contest_system_id):
        args = parser_change.parse_args()
        id_in_contest_system = args['id_in_contest_system']

        pupil = Pupil.get_entity_or_404(pupil_id)
        contest_system = ContestSystem.get_entity_or_404(contest_system_id)

        session = create_session()

        contest_system_to_pupil = session.query(ContestSystemToPupil).filter(
            ContestSystemToPupil.contest_system_id == contest_system_id,
            ContestSystemToPupil.pupil_id == pupil_id).first()

        contest_system_to_pupil_exist = True

        if contest_system_to_pupil is None:
            contest_system_to_pupil_exist = False

            contest_system_to_pupil = ContestSystemToPupil()
            contest_system_to_pupil.pupil = pupil
            contest_system_to_pupil.contest_system = contest_system

        contest_system_to_pupil.id_on_contest_system = id_in_contest_system

        if contest_system_to_pupil_exist:
            session.merge(contest_system_to_pupil)
        else:
            session.add(contest_system_to_pupil)

        session.commit()
