from flask_restful import reqparse


def to_bool(data):
    return bool(int(data))


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str.strip)
parser.add_argument('is_active', required=True, type=to_bool)
parser.add_argument('subject_id', required=True, type=int)
parser.add_argument('teacher_id', required=True, type=int)
