from flask_restful import reqparse
from app.api.parsers_data_checker.checkers import CheckName, CheckSurname, CheckEmail, CheckPassword

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=CheckName().check_string)
parser.add_argument('surname', required=True, type=CheckSurname().check_string)
parser.add_argument('email', required=True, type=CheckEmail().check_string)
parser.add_argument('password', required=True, type=CheckPassword().check_string)
parser.add_argument('confident_info')

parser_role = reqparse.RequestParser()
parser_role.add_argument("id", required=True, type=int)
parser_role.add_argument("role", required=True)
