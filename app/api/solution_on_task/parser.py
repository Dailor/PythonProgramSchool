from flask_restful.reqparse import RequestParser

parser = RequestParser()
parser.add_argument('task_id', required=True, type=int)
parser.add_argument('group_id', required=True, type=int)
