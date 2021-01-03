from app.config_app import PaginationConfig
from app.api.utils.parser.checkers import CheckName, CheckSurname, CheckEmail, CheckPassword
from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=CheckName.check_string)
parser.add_argument('surname', required=True, type=CheckSurname.check_string)
parser.add_argument('email', required=True, type=CheckEmail.check_string)
parser.add_argument('password', required=True, type=CheckPassword.check_string)
parser.add_argument('role_id', required=True, type=int)
parser.add_argument('confident_info')

# parser_get_users = reqparse.RequestParser()
# parser_get_users.add_argument('offset', default=0, type=int)
# parser_get_users.add_argument('count', default=10, type=lambda x: min(int(x), PaginationConfig.MAX_COUNT))
