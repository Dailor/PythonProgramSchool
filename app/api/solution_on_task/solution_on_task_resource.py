from .parser import parser

from app.models.__all_models import Task, Solution, TaskCheckStatus, Group
from app.models import db_session

from flask import jsonify
from flask_restful import Resource, abort
from flask_login import current_user


class SolutionOnTask(Resource):
    def get(self):
        args = parser.parse_args()
        group_id = args['group_id']
        task_id = args['task_id']

        session = db_session.create_session()

        Group.get_entity_or_404(group_id)

        pupil = current_user.pupil
        task = Task.get_entity_or_404(task_id)

        pupil_solutions_on_task = session.query(Solution).filter(Solution.task_id == task.id,
                                                                 Solution.group_id == group_id,
                                                                 Solution.pupil_id == pupil.id).all()

        can_see_solution = False

        for solution in pupil_solutions_on_task:
            if solution.review_status is TaskCheckStatus.ACCESS:
                can_see_solution = True
                break

        if len(pupil_solutions_on_task) >= task.tries_count:
            can_see_solution = True

        if can_see_solution:
            return jsonify({'solution': task.solutions})
        else:
            return abort(403)
