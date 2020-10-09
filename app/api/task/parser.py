from flask_restful import reqparse
from flask_restful import inputs

parser = reqparse.RequestParser()
parser.add_argument('group_id', type=int, required=True)
parser.add_argument('task_id', type=int, required=True)
parser.add_argument('result')

parser_solutions_list_for_task = reqparse.RequestParser()
parser_solutions_list_for_task.add_argument('pupil_id', type=int, required=True, location='args')
parser_solutions_list_for_task.add_argument('group_id', type=int, required=True, location='args')
parser_solutions_list_for_task.add_argument('task_id', type=int, required=True, location='args')

parser_solution_for_task = reqparse.RequestParser()
parser_solution_for_task.add_argument('solution_id', type=int, required=True, location='args')

parser_solution_status_change = reqparse.RequestParser()
parser_solution_status_change.add_argument("solution_id", type=int, required=True)
parser_solution_status_change.add_argument("review_status", type=inputs.boolean, required=True)
