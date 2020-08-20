from models import db_session
from models.user import User, Role, UserRoles, FAKE_PASSWORD
from models.teacher import Teacher
from models.pupil import Pupil
from models.subject import Subject
from models.group import Group

from forms.teacher_edit import TeacherEditForm

from flask import blueprints as bl_module
from flask import render_template, redirect, abort, jsonify, request
from werkzeug.exceptions import Forbidden, NotImplemented, BadRequest
from flask_login import current_user

blueprint = bl_module.Blueprint("admin", __name__, template_folder="templates", static_folder="static")


def user_serializer(user):
    user_serialized = user.to_dict(rules=('-hashed_password', '-pupil', '-teacher', '-roles'))
    user_serialized['password'] = FAKE_PASSWORD
    user_serialized['roles'] = user.one_string_all_roles()
    return user_serialized


def teacher_serializer(teacher):
    teacher_serialized = user_serializer(teacher.user)
    teacher_serialized['id'] = teacher.id
    teacher_serialized['groups'] = '\n'.join(teacher.get_string_groups())
    teacher_serialized['subjects'] = '\n'.join(teacher.get_string_subjects())

    return teacher_serialized


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


@blueprint.route("/api_user", methods=["GET"])
def get_users():
    roles = request.args.get("role")
    session = db_session.create_session()

    if roles is None:
        users = session.query(User)
    else:
        roles = roles.strip().replace(", ", ",").upper().split(",")
        users = session.query(User).join(Role).filter(Role.name.in_(roles))

    users_serialized = list()
    for user in users:
        users_serialized.append(user_serializer(user))

    return jsonify({'users': users_serialized})


@blueprint.route("/api_user", methods=["PUT"])
def add_user():
    name = request.values["name"].strip()
    surname = request.values["surname"].strip()
    email = request.values["email"].strip()
    confident_info = request.values["confident_info"].strip()
    password = request.values["password"]

    if not len(name):
        return jsonify({"error": "Поле с именем обязательно"}), BadRequest.code
    if not len(surname):
        return jsonify({"error": "Поле с фамилией обязательно"}), BadRequest.code
    if not len(email):
        return jsonify({"error": "Поле с почтой обязательно"}), BadRequest.code
    if len(password) < 6:
        return jsonify({"error": "Пароль минимум из 6 символов"}), BadRequest.code
    elif len(''.join(password.split(maxsplit=1))) != len(password):
        return jsonify({"error": "поле с паролем не может содержать пробельный символ"})

    session = db_session.create_session()

    if session.query(User).filter(User.email == email).first() is not None:
        return jsonify({"error": "Пользователь с таким email'ом уже существует"}), NotImplemented.code

    user = User()
    user.name = name
    user.surname = surname
    user.email = email
    user.confident_info = confident_info
    user.set_password(password)

    session.add(user)
    session.commit()

    return jsonify(user_serializer(user))


@blueprint.route("/api_user", methods=["POST"])
def edit_user():
    user_id = int(request.values["id"])
    name = request.values["name"]
    surname = request.values["surname"]
    email = request.values["email"]
    confident_info = request.values["confident_info"]
    password = request.values["password"]

    if not len(name):
        return jsonify({"error": "Поле с именем обязательно"}), BadRequest
    if not len(surname):
        return jsonify({"error": "Поле с фамилией обязательно"}), BadRequest
    if not len(email):
        return jsonify({"error": "Поле с почтой обязательно"}), BadRequest
    if not len(password):
        return jsonify({"error": "Поле с паролем обязательно"}), BadRequest

    session = db_session.create_session()

    user = session.query(User).get(user_id)

    if user is None:
        return jsonify({"error": "Пользователь с таким ID не найден"}), BadRequest.code

    user_check_email = session.query(User).filter(User.email == email).first()
    if user_check_email is not None and user_check_email.id != user.id:
        return jsonify({"error": "Уже существует пользователь с таким email'ом"}), NotImplemented.code

    user.name = name
    user.surname = surname
    user.email = email
    user.confident_info = confident_info

    if FAKE_PASSWORD != password:
        user.set_password(password)

    session.merge(user)
    session.commit()

    return jsonify(user_serializer(user))


@blueprint.route("/api_user/set_role", methods=["POST"])
def role_setter():
    session = db_session.create_session()

    role_name = request.values["set_role"].upper()
    user_id = int(request.values["id"])

    if not UserRoles.check_role_in_roles(role_name):
        return jsonify({"error": "Такой роли нет"}), BadRequest.code

    user = session.query(User).get(user_id)
    if user is None:
        return jsonify({"error": "Пользователь с таким ID не найден"}), BadRequest.code

    if user.check_role(role_name):
        return jsonify({"error": "Пользователь уже имею данную роль"}), NotImplemented.code

    role = Role()
    role.name = role_name
    user.roles.append(role)

    if role_name == UserRoles.TEACHER:
        teacher = Teacher()
        user.teacher = teacher
    elif role_name == UserRoles.PUPIL:
        pupil = Pupil()
        user.pupil = pupil

    session.merge(user)
    session.commit()

    return jsonify(user_serializer(user))


@blueprint.route("/api_teacher")
def get_teachers():
    session = db_session.create_session()

    teachers = session.query(Teacher).all()

    return jsonify({"teachers": [teacher_serializer(teacher) for teacher in teachers]})


@blueprint.route("/teachers/edit/<int:teacher_id>", methods=["GET", "POST"])
def edit_teacher_page(teacher_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)

    if teacher is None:
        return abort(404)

    session = db_session.create_session()

    form = TeacherEditForm()

    subjects = session.query(Subject)
    groups = session.query(Group).filter(Group.teacher_id is None)

    form.subjects.choices = [(subject.id, subject.name) for subject in subjects]
    form.groups.choices = [(group.id, group.name) for group in groups]

    return render_template("admin/teacher_edit.html", form=form)
