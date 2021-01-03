from .teacher import Teacher
from .pupil import Pupil

from .db_helper import DbHelper
from .db_session import SqlAlchemyBase, create_session
from app.config_app import BaseConfig

import sqlalchemy
import jwt

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeSerializer
from flask_restful import abort
from flask_login import UserMixin

from time import time
from fast_enum import FastEnum

url_serializer = URLSafeSerializer(BaseConfig.SECRET_KEY)


class UserRoles(metaclass=FastEnum):
    __slots__ = ('id', 'text',)

    WITHOUT_ROLE = 0, 'Нет роли'
    ADMIN = 1, "Админ"
    TEACHER = 2, "Учитель"
    PUPIL = 3, "Ученик"

    def __init__(self, value, text, name):
        self.name = name
        self.value = value
        self.id = value
        self.text = text

    @staticmethod
    def all_roles():
        return {role.value: role.text for role in UserRoles._value_to_instance_map.values()}


FAKE_PASSWORD = "PASSWORD"


class User(SqlAlchemyBase, UserMixin, SerializerMixin, DbHelper):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)

    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    _email = sqlalchemy.Column(sqlalchemy.String(255), name='email',
                               nullable=False, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(150), nullable=False)

    about_user = sqlalchemy.Column(sqlalchemy.Text, default="Soon here will be information about me.")
    confident_info = sqlalchemy.Column(sqlalchemy.Text, default="")

    teacher = orm.relationship("Teacher", lazy='joined', uselist=False, back_populates='user',
                               cascade="all, delete-orphan",
                               single_parent=True,
                               passive_deletes=True)
    pupil = orm.relationship("Pupil", lazy='joined', uselist=False, back_populates='user',
                             cascade="all, delete-orphan",
                             single_parent=True,
                             passive_deletes=True)
    admin = orm.relationship("Admin", lazy='joined', uselist=False, back_populates='user',
                             cascade="all, delete-orphan",
                             single_parent=True,
                             passive_deletes=True)

    def get_id(self):
        return str(self.session_id)

    @property
    def role_id(self):
        role_id = UserRoles.WITHOUT_ROLE.value

        if self.is_admin:
            role_id = UserRoles.ADMIN.value
        elif self.is_teacher:
            role_id = UserRoles.TEACHER.value
        elif self.is_pupil:
            role_id = UserRoles.PUPIL.value

        return role_id

    @property
    def full_name(self):
        return (self.surname + " " + self.name).strip()

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        session = create_session()

        already_with_email = session.query(User).filter(User.email == email).first()
        if already_with_email and already_with_email.id != self.id:
            return abort(403, message='Пользователь с такой почтой существует')

        self._email = email.strip()
        if self.hashed_password is not None:
            self.session_id = url_serializer.dumps([self.email, self.hashed_password])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        if self.email is not None:
            self.session_id = url_serializer.dumps([self.email, self.hashed_password])

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            BaseConfig.SECRET_KEY, algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, BaseConfig.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except Exception as e:
            return
        session = create_session()
        return session.query(User).get(id)

    def set_role(self, role_id):
        if self.id == BaseConfig.ADMIN_DEFAULT_ID and role_id != UserRoles.ADMIN.value:
            return abort(403, message='Нельзя менять роль у первого админа')

        if role_id == UserRoles.ADMIN.value:
            if not self.is_admin:
                self.admin = Admin()
                self.remove_roles(self.teacher, self.pupil)

        elif role_id == UserRoles.TEACHER.value:
            if not self.is_teacher:
                self.teacher = Teacher()
                self.remove_roles(self.admin, self.pupil)

        elif role_id == UserRoles.PUPIL.value:
            if not self.is_pupil:
                self.pupil = Pupil()
                self.remove_roles(self.admin, self.teacher)

        elif role_id == UserRoles.WITHOUT_ROLE.value:
            self.remove_roles(self.admin, self.teacher, self.pupil)

        else:
            return abort(404, message='Роль не найдена')

    def remove_roles(*role_instances):
        session = create_session()

        for role_instance in role_instances:
            if any(isinstance(role_instance, role) for role in [Admin, Pupil, Teacher]):
                session.delete(role_instance)

    @property
    def is_admin(self):
        return self.admin is not None

    @property
    def is_pupil(self):
        return self.pupil is not None

    @property
    def is_teacher(self):
        return self.teacher is not None

    @property
    def is_have_role(self):
        return self.is_admin or self.is_teacher or self.is_pupil

    def get_string_role(self):
        role_string = UserRoles.WITHOUT_ROLE.text

        if self.is_admin:
            role_string = UserRoles.ADMIN.text
        elif self.is_teacher:
            role_string = UserRoles.TEACHER.text
        elif self.is_pupil:
            role_string = UserRoles.PUPIL.text

        return role_string.title()

    def check_role(self, check_role):
        return self.get_string_role().lower() == check_role

    def __eq__(self, other):
        return self.id == other.id


class Admin(SqlAlchemyBase):
    __tablename__ = 'admins'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id", ondelete='CASCADE'),
                                primary_key=True)
    user = orm.relationship("User", back_populates='admin')
