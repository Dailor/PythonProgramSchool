from flask_restful import reqparse


def min_one_length_str(string):
    if len(string):
        return string
    raise ValueError("Название категории должно состоять минимум из одного символа")


parser_for_teacher = reqparse.RequestParser()
parser_for_teacher.add_argument("name", type=min_one_length_str, required=True)

parser_for_admin = parser_for_teacher.copy()
parser_for_admin.add_argument('author_teacher_id', required=True, type=int)
parser_for_admin.add_argument("groups_id[]", required=False, type=int, action='append', default=[])
