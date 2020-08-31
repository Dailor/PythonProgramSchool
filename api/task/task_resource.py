from models.pupil import Pupil
from models.task import Task, Solutions, TaskCheckStatusString, TaskCheckStatus
from models.group import Group
from models import db_session

from api.group.group_resource import check_group_by_id
from api.pupils.pupil_resource import check_pupil_by_id

from .parser import parser

from flask import jsonify
from flask_restful import Resource, abort
from flask_login import current_user


def check_task_by_id(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)

    if task is None:
        abort(404, error=f'Задача с {task_id} ID не найдена')


class SolutionsListResource(Resource):
    def get(self, group_id, task_id):
        pupil_to_dict_rules = ('-groups',)

        check_task_by_id(task_id)
        check_group_by_id(group_id)

        session = db_session.create_session()
        group = session.query(Group).get(group_id)

        pupils_solutions_info = dict()
        pupils_tried_to_solve = dict()

        for status, string_status in zip(TaskCheckStatus.ALL_STATUS, TaskCheckStatusString.ALL_STATUS):
            solutions = session.query(Solutions).filter(Solutions.task_id == task_id,
                                                        Solutions.group_id == group_id,
                                                        Solutions.review_status == status).order_by(Solutions.id.desc())

            solutions_for_string_status = pupils_solutions_info[string_status] = list()
            double_check = dict()

            for solution in solutions:
                if solution.pupil.id not in double_check:
                    pupil_dict = solution.pupil.to_dict(rules=pupil_to_dict_rules)
                    pupil_dict['solution_id'] = solution.id

                    solutions_for_string_status.append(pupil_dict)
                    pupils_tried_to_solve[solution.pupil_id] = string_status
                    double_check[solution.pupil_id] = True

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

        solution = Solutions()
        solution.task_id = task_id
        solution.group_id = group_id
        solution.pupil = pupil
        solution.result = args['result']

        session.add(session.merge(solution))
        session.commit()

        return jsonify({'success': 'success'})
