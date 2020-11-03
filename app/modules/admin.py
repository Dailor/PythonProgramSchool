from app.models import db_session
from app.models.__all_models import Topic

from app.api.user.user_resource import UserListResource, UserResource, RoleSetterResource
from app.api.group.group_resource import GroupListResource, GroupResource, GroupsToDict
from app.api.teacher.teacher_resource import TeacherListResource, TeacherDictIdToFullName, TeacherResource
from app.api.pupils.pupil_resource import PupilListResource, PupilResource
from app.api.subject.subject_resource import SubjectListResource, SubjectDictIdToName, SubjectResource
from app.api.topics.topic_resource import TopicListResource, TopicResource

from flask import blueprints as bl_module
from flask import render_template, redirect, abort
from flask_login import current_user
from flask_restful import Api
from werkzeug.exceptions import Forbidden

blueprint = bl_module.Blueprint("admin", __name__, template_folder="templates", static_folder="static")
api = Api(blueprint)

api.add_resource(UserListResource, '/api_user')
api.add_resource(UserResource, '/api_user/<int:user_id>')
api.add_resource(RoleSetterResource, '/api_user/role')

api.add_resource(GroupResource, '/api_group/<int:group_id>')
api.add_resource(GroupListResource, '/api_group')

api.add_resource(TeacherResource, '/api_teacher/<int:teacher_id>')
api.add_resource(TeacherListResource, '/api_teacher')

api.add_resource(PupilResource, '/api_pupil/<int:pupil_id>')
api.add_resource(PupilListResource, '/api_pupil')

api.add_resource(SubjectResource, '/api_subject/<int:subject_id>')
api.add_resource(SubjectListResource, '/api_subject')

api.add_resource(TopicListResource, '/api_topic')
api.add_resource(TopicResource, '/api_topic/<int:topic_id>')


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


@blueprint.route('/pupils')
def pupils_table():
    groups_dict = GroupsToDict().get_groups_dict()
    return render_template("admin/pupils.html", groups_dict=groups_dict)


@blueprint.route('/subjects')
def subjects_table():
    return render_template("admin/subjects.html")


@blueprint.route('/groups')
def groups_table():
    session = db_session.create_session()

    teachers_dict = TeacherDictIdToFullName().teachers_dict()
    subjects_dict = SubjectDictIdToName().subjects_dict()
    topics_dict = {topic.id: topic.name for topic in session.query(Topic).all()}

    return render_template("admin/groups.html", teachers_dict=teachers_dict, subjects_dict=subjects_dict,
                           topics_dict=topics_dict)


@blueprint.route('/topics')
def topics_table():
    teachers_dict = TeacherDictIdToFullName().teachers_dict()
    groups_dict = GroupsToDict().get_groups_dict()
    return render_template("admin/topics.html", teachers_dict=teachers_dict, groups_dict=groups_dict)
