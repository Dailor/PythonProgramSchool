from flask_restful import reqparse


def to_bool(data):
    return bool(int(data))


def id_list(data):
    result = list()

    for i in data:
        result.append(int(i))

    return result


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str.strip, location='json')
parser.add_argument('is_active', required=True, type=to_bool, location='json')
parser.add_argument('subject_id', required=True, type=int, location='json')
parser.add_argument('courses_id', required=True, type=id_list, location='json')

parser_admin = parser.copy()
parser_admin.add_argument('teacher_id', required=True, type=int, location='json')