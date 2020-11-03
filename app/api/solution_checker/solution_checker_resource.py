from app.models import db_session
from app.models.__all_models import Submission, Solutions, ApiCheckAnswers, TaskInfoFields
from flask_restful import Resource
from flask import request


class SolutionCheckerResource(Resource):
    def put(self):

        solution_id = int(request.args['solution_id'])

        session = db_session.create_session()

        solution = session.query(Solutions).get(solution_id)

        if solution is None:
            return

        submission_results = request.json

        submission = Submission()

        submission.token_sub = submission_results['token']
        submission.time = submission_results['time']
        submission.memory = submission_results['memory']
        submission.status = submission_results['status']
        submission.stderr = submission_results['stderr']

        if int(submission.status['id']) == ApiCheckAnswers.ACCEPT:
            solution.solution_info[TaskInfoFields.ACCEPT] = solution.solution_info[TaskInfoFields.ACCEPT] + 1
        else:
            solution.solution_info[TaskInfoFields.FAILED] = solution.solution_info[TaskInfoFields.FAILED] + 1

        checked_tests_count = solution.solution_info[TaskInfoFields.ACCEPT] + solution.solution_info[
            TaskInfoFields.FAILED]

        if checked_tests_count == solution.solution_info[TaskInfoFields.COUNT]:
            if solution.solution_info[TaskInfoFields.ACCEPT] == checked_tests_count:
                solution.review_status = True
            else:
                solution.review_status = False

        submission.solution_id = solution_id

        session.merge(solution)
        session.add(submission)
        session.commit()
