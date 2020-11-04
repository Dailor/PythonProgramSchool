from app.config_app import CheckerConfig

from app.models.__all_models import Task, Solutions, TaskCheckStatusString, TaskCheckStatus, TaskInfoFields, Group, \
    SubmissionsBatch
from ...models import db_session

from app.api.group.group_resource import check_group_by_id
from app.api.pupils.pupil_resource import check_pupil_by_id

from .parser import parser, parser_solution_for_task, parser_solutions_list_for_task, parser_solution_status_change

import requests
import json

from flask import jsonify
from flask_restful import Resource, abort
from flask_login import current_user


def check_task_by_id(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)

    if task is None:
        abort(404, error=f'Задача с {task_id} ID не найдена')


def check_solution_by_id(solution_id):
    session = db_session.create_session()

    solution = session.query(Solutions).get(solution_id)
    if solution is None:
        abort(404, error=f'Решение с {solution_id} ID не найдено')


def check_permission(user, group_id):
    if user.is_teacher is False:
        abort(403, 'Нужно хотя бы являтся учителем')

    session = db_session.create_session()

    teacher = user.teacher

    group = session.query(Group).get(group_id)

    if teacher.id != group.teacher_id:
        abort(403, f'Вы не ведет у группы с {group_id} ID')


class SolutionsListResource(Resource):
    def get(self, group_id, task_id):
        pupil_to_dict_rules = ('-groups',)

        check_task_by_id(task_id)
        check_group_by_id(group_id)

        session = db_session.create_session()
        group = session.query(Group).get(group_id)

        pupils_solutions_info = dict()
        pupils_tried_to_solve = dict()
        pupil_solved = dict()

        for status, string_status in zip(TaskCheckStatus.ALL_STATUS, TaskCheckStatusString.ALL_STATUS):
            solutions = session.query(Solutions).filter(Solutions.task_id == task_id,
                                                        Solutions.group_id == group_id,
                                                        Solutions.review_status == status).order_by(Solutions.id.desc())

            solutions_for_string_status = pupils_solutions_info[string_status] = list()
            double_check = dict()

            for solution in solutions:
                if solution.pupil.id not in double_check:
                    if status == TaskCheckStatus.FAILED and pupil_solved.get(solution.pupil_id, False):
                        continue

                    pupil_dict = solution.pupil.to_dict(rules=pupil_to_dict_rules)
                    pupil_dict['solution_id'] = solution.id

                    solutions_for_string_status.append(pupil_dict)
                    pupils_tried_to_solve[solution.pupil_id] = string_status
                    double_check[solution.pupil_id] = True

                    if status == TaskCheckStatus.ACCESS:
                        pupil_solved[solution.pupil_id] = True

        pupils_solutions_info[TaskCheckStatusString.NOT_PASS] = [pupil.to_dict(rules=pupil_to_dict_rules) for pupil in
                                                                 group.pupils if
                                                                 not pupils_tried_to_solve.get(pupil.id, False)]

        return jsonify(pupils_solutions_info)

    def put(self):
        args = parser.parse_args()

        group_id = args['group_id']
        task_id = args['task_id']

        check_group_by_id(group_id)
        check_task_by_id(task_id)

        session = db_session.create_session()

        group = session.query(Group).get(group_id)
        pupil = current_user.pupil

        if pupil is None or pupil not in group.pupils:
            abort(403)

        task = session.query(Task).get(task_id)

        solutions_passed = session.query(Solutions).filter(Solutions.pupil_id == pupil.id,
                                                           Solutions.group_id == group_id,
                                                           Solutions.task_id == task_id).order_by(Solutions.id).all()
        tries_left = task.tries_count - len(solutions_passed)

        if tries_left <= 0:
            abort(403, error='У вас закончились попытки')

        solution = Solutions()
        solution.task_id = task_id
        solution.group_id = group_id
        solution.pupil = pupil
        solution.result = args['result']

        task.api_check = True

        if task.api_check:
            submission_batch = SubmissionsBatch()
            submission_batch.solution = solution
            submission_batch.all_tasks_count = task.get_tests_count()
            session.flush()
            self.send_task_to_checker(solution, task, submission_batch.id)

        session.add(submission_batch)
        session.add(solution)
        session.commit()

        return jsonify({'success': 'success', **solution.to_dict(only=('id', 'date_delivery', 'review_status'))})

    def send_task_to_checker(self, solution, task, submission_batch_id):
        callback_url = CheckerConfig.CALLBACK_URL
        params_callback_url = {
            'SECRET_KEY': CheckerConfig.SECRET_KEY,
            'submission_batch_id': submission_batch_id
        }

        data_one = {'source_code': solution.result,
                    'language_id': task.language_id,
                    'cpu_time_limit': task.time_sec,
                    'memory_limit': task.memory_mb * 1000
                    }

        submissions = list()

        tests = [*task.examples, *task.examples_hidden]

        for i in range(len(tests)):
            test = tests[i]

            in_data = test['in_data']
            out_data = test['out_data']

            submission = data_one.copy()
            submission['stdin'] = in_data
            submission['expected_output'] = out_data
            submission['callback_url'] = callback_url + '?' + '&'.join(f'{param}={value}'
                                                                       for param, value in params_callback_url.items())

            submissions.append(submission)

        json_data = {'submissions': submissions}

        r = requests.post(CheckerConfig.BATCH_SUBS_URL, headers=CheckerConfig.HEADERS, json=json_data)
        return r


class PupilSolutionsListForTask(Resource):
    def get(self):
        args = parser_solutions_list_for_task.parse_args()

        pupil_id = args['pupil_id']
        group_id = args['group_id']
        task_id = args['task_id']

        check_pupil_by_id(pupil_id)
        check_group_by_id(group_id)
        check_task_by_id(task_id)

        session = db_session.create_session()
        task = session.query(Task).get(task_id)

        solutions = session.query(Solutions).filter(Solutions.pupil_id == pupil_id, Solutions.group_id == group_id,
                                                    Solutions.task_id == task_id).order_by(Solutions.id).all()
        tries_left = task.tries_count - len(solutions)
        return jsonify(
            {"solutions": [solution.to_dict(only=('id', 'date_delivery', 'review_status', 'solution_info', 'result'))
                           for solution
                           in solutions],
             "tries_left": tries_left})


class PupilSolutionForTask(Resource):
    def get(self):
        args = parser_solution_for_task.parse_args()

        solution_id = args['solution_id']

        check_solution_by_id(solution_id)

        session = db_session.create_session()
        solution = session.query(Solutions).get(solution_id)

        return jsonify(solution.to_dict(only=('id', 'result', 'date_delivery', 'review_status', 'solution_info')))

    def post(self):
        args = parser_solution_status_change.parse_args()

        solution_id = args['solution_id']
        review_status = args['review_status']

        check_solution_by_id(solution_id)

        session = db_session.create_session()

        solution = session.query(Solutions).get(solution_id)

        check_permission(current_user, solution.group_id)

        solution.review_status = review_status

        session.merge(solution)
        session.commit()

        return jsonify(solution.to_dict(only=('id', 'date_delivery', 'review_status', 'solution_info')))
