from ..utils.parser.checkers import to_bool, id_list

from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, trim=True, location='json')
parser.add_argument('is_active', required=True, type=to_bool, location='json')
parser.add_argument('courses_id', required=True, type=id_list, location='json')

parser_admin = parser.copy()
parser_admin.add_argument('teacher_id', required=True, type=int, location='json')