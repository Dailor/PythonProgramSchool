from api.user.user_resource import UserListResource, UserResource, RoleSetterResource
from api.group.group_resource import GroupListResource, GroupResource
from api.teacher.teacher_resource import TeacherListResource, TeacherDictIdToFullName
from api.subject.subject_resource import SubjectListResource, SubjectDictIdToName

from flask import blueprints as bl_module
from flask import render_template, redirect, abort, jsonify, request
from flask_login import current_user
from flask_restful import Api
from werkzeug.exceptions import Forbidden, NotImplemented, BadRequest

blueprint = bl_module.Blueprint("admin", __name__, template_folder="templates", static_folder="static")
api = Api(blueprint)

api.add_resource(UserListResource, '/api_user')
api.add_resource(UserResource, '/api_user/<int:user_id>')
api.add_resource(RoleSetterResource, '/api_user/role')

api.add_resource(GroupListResource, '/api_group')
api.add_resource(GroupResource, '/api_group/<int:group_id>')

api.add_resource(TeacherListResource, '/api_teacher')
api.add_resource(TeacherDictIdToFullName, '/api_teacher/get_dict')

api.add_resource(SubjectListResource, '/api_subject')
api.add_resource(SubjectDictIdToName, '/api_subject/get_dict')


@blueprint.before_request
def before_request_func():
    if not current_user.is_authenticated:
        return redirect("/login")
    if not current_user.is_admin:
        return abort(Forbidden.code)


@blueprint.route("/users")
def users_table():
    return render_template("admin/users.html")


@blueprint.route("/admins")
def admins_table():
    return render_template("admin/admins.html")


@blueprint.route("/teachers")
def teachers_table():
    return render_template("admin/teachers.html")


@blueprint.route('/subjects')
def subjects_table():
    return render_template("admin/subjects.html")


@blueprint.route('/groups')
def groups_table():
    return render_template("admin/groups.html")
