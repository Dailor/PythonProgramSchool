from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument('author_teacher_id', required=True, type=int)
parser.add_argument("groups_id[]", required=False, type=int, action='append', default=[])
