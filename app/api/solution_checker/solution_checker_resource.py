from app.models import db_session
from app.models.__all_models import Submission, Solutions, ApiCheckAnswers, TaskInfoFields, SubmissionsBatch
from flask_restful import Resource
from flask import request


class SolutionCheckerResource(Resource):
    def put(self):

        submission_batch_id = int(request.args['submission_batch_id'])

        session = db_session.create_session()

        submission_batch = session.query(SubmissionsBatch).get(submission_batch_id)

        if submission_batch is None:
            return

        submission_results = request.json

        submission = Submission()

        submission.token_sub = submission_results['token']
        submission.time = submission_results['time']
        submission.memory = submission_results['memory']
        submission.status = submission_results['status']
        submission.stderr = submission_results['stderr']

        if int(submission.status['id']) == ApiCheckAnswers.ACCEPT:
            submission_batch.accepted_tasks_count += 1
        else:
            submission_batch.failed_tasks_count += 1

        checked_tests_count = submission_batch.get_checked_count()

        if checked_tests_count == submission_batch.all_tasks_count:
            if submission_batch.accepted_tasks_count == checked_tests_count:
                submission_batch.solution.review_status = True
            else:
                submission_batch.solution.review_status = False
            submission_batch.solution.solution_info = submission_batch.get_statistic()

        submission_batch.submissions.append(submission)
        session.merge(submission_batch)
        session.commit()
