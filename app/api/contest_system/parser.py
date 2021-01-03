from flask_restful.reqparse import RequestParser

parser_change = RequestParser()
parser_change.add_argument('id_in_contest_system', required=True, location='json')
