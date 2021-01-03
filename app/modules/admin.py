from app.models import db_session
from app.models.__all_models import UserRoles, Course, Teacher, Group

from app.api.user.user_resource import UserListResource, UserResource
from app.api.group.group_resource import GroupListResource, GroupResource
from app.api.teacher.teacher_resource import TeacherListResource, TeacherResource
from app.api.pupils.pupil_resource import PupilListResource, PupilResource
from app.api.course.course_resource import CourseListResource, CourseResource

from flask import blueprints as bl_module
from flask import render_template, redirect, abort
from flask_login import current_user
from flask_restful import Api
from werkzeug.exceptions import Forbidden

blueprint = bl_module.Blueprint("admin", __name__, template_folder="templates", static_folder="static")
api = Api(blueprint, prefix='/api')


def register_resources():
    api.add_resource(UserListResource, '/user')
    api.add_resource(UserResource, '/user/<int:user_id>')

    api.add_resource(TeacherResource, '/teacher/<int:teacher_id>')
    api.add_resource(TeacherListResource, '/teacher')

    api.add_resource(PupilResource, '/pupil/<int:pupil_id>')
    api.add_resource(PupilListResource, '/pupil')

    api.add_resource(GroupResource, '/group/<int:group_id>')
    api.add_resource(GroupListResource, '/group')

    api.add_resource(CourseListResource, '/course')
    api.add_resource(CourseResource, '/course/<int:course_id>')





@blueprint.before_request
def before_request_func():
    if not current_user.is_authenticated:
        return redirect("/login")
    if not current_user.is_admin:
        return abort(Forbidden.code)


@blueprint.route("/users")
def users_table():
    return render_template("admin/users.html", all_roles=UserRoles.all_roles())


@blueprint.route("/admins")
def admins_table():
    return render_template("admin/admins.html")


@blueprint.route("/teachers")
def teachers_table():
    return render_template("admin/teachers.html")


@blueprint.route('/pupils')
def pupils_table():
    session = db_session.create_session()
    groups_dict = {group.id: group.name for group in session.query(Group).all()}
    return render_template("admin/pupils.html", groups_dict=groups_dict)

@blueprint.route('/groups')
def groups_table():
    session = db_session.create_session()

    teachers_dict = {teacher.id: teacher.user.full_name for teacher in session.query(Teacher).all()}
    courses_dict = {course.id: course.name for course in session.query(Course).all()}

    return render_template("admin/groups.html", teachers_dict=teachers_dict,
                           courses_dict=courses_dict)


@blueprint.route('/courses')
def courses_table():
    session = db_session.create_session()

    teachers_dict = {teacher.id: teacher.user.full_name for teacher in session.query(Teacher).all()}
    groups_dict = {group.id: group.name for group in session.query(Group).all()}

    return render_template("admin/courses.html", teachers_dict=teachers_dict, groups_dict=groups_dict)


register_resources()
