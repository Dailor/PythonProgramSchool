from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument("name", required=True, type=str, location='json')
parser.add_argument('tasks', required=True, type=list, location='json')
parser.add_argument('html_page', required=False, location='json')
parser.add_argument('language_id', required=True, location='json')

parser_lesson_available = reqparse.RequestParser()
parser_lesson_available.add_argument('group_id', required=True, type=int)
parser_lesson_available.add_argument('lesson_id', required=True, type=int)

parser_lesson_available_contest = parser_lesson_available.copy()
parser_lesson_available_contest.add_argument('deadline', required=True, type=int)