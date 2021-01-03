from flask_restful import reqparse



parser = reqparse.RequestParser()
parser.add_argument('groups_id[]', type=int, action='append', default=[])
