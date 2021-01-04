from flask_restful import reqparse

from ..utils.parser.checkers import id_list


def min_one_length_str(string):
    if len(string):
        return string
    raise ValueError("Название категории должно состоять минимум из одного символа")


parser_for_teacher = reqparse.RequestParser()
parser_for_teacher.add_argument("name", type=min_one_length_str, required=True, location=('json', 'values'))

parser_for_admin = parser_for_teacher.copy()
parser_for_admin.add_argument('curators_id', required=True, type=id_list, location='json')
