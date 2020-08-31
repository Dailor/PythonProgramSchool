from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('group_id', type=int, required=True)
parser.add_argument('task_id', type=int, required=True)
parser.add_argument('result')
