import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


def title_return_string(func):
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)
        return func_result.title() if isinstance(func_result, str) else func_result

    return wrapper


class UserRoles:
    ADMIN = "админ"
    TEACHER = "учитель"
    PUPIL = "ученик"

    WITHOUT_ROLE = None
    ALL_ROLES = [ADMIN, TEACHER, PUPIL]

    @staticmethod
    def get_title_all_roles():
        return [role.title() for role in UserRoles.ALL_ROLES]


FAKE_PASSWORD = "PASSWORD"


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    email = sqlalchemy.Column(sqlalchemy.String(255),
                              nullable=False, index=True, unique=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String(150), nullable=False)

    about_user = sqlalchemy.Column(sqlalchemy.Text, default="Soon here will be information about me.")
    confident_info = sqlalchemy.Column(sqlalchemy.Text, default="")

    teacher = orm.relationship("Teacher", lazy='joined', uselist=False, back_populates='user')
    pupil = orm.relationship("Pupil", lazy='joined', uselist=False, back_populates='user')
    admin = orm.relationship("Admin", lazy='joined', uselist=False, back_populates='user')

    @property
    def full_name(self):
        return self.surname + " " + self.name

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def check_role(self, check_role):
        return self.get_string_role().lower() == check_role

    @title_return_string
    def get_string_role(self):
        return UserRoles.ADMIN if self.is_admin else \
            UserRoles.TEACHER if self.is_teacher else \
                UserRoles.PUPIL if self.is_pupil else \
                    UserRoles.WITHOUT_ROLE

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


class Admin(SqlAlchemyBase):
    __tablename__ = 'admins'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    user = orm.relationship("User", back_populates='admin')
