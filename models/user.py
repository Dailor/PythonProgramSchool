import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase, create_session


class UserRoles:
    ADMIN = "ADMIN"
    PUPIL = "PUPIL"
    TEACHER = "TEACHER"

    @staticmethod
    def check_role_in_roles(role):
        return role in UserRoles.ALL_ROLES


UserRoles.ALL_ROLES = [k for k, v in vars(UserRoles).items() if not k.startswith("_")]
FAKE_PASSWORD = "PASSWORD"


class Role(SqlAlchemyBase):
    __tablename__ = "roles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User")


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

    teacher = orm.relationship("Teacher", uselist=False)
    pupil = orm.relationship("Pupil", uselist=False)

    roles = orm.relationship("Role")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def check_role(self, check_role):
        return any(check_role == role.name for role in self.roles)

    def get_string_roles(self):
        return [role.name for role in self.roles]

    def one_string_all_roles(self):
        return ', '.join(self.get_string_roles())

    @property
    def full_name(self):
        return self.surname + " " + self.name

    @property
    def is_admin(self):
        return self.check_role(UserRoles.ADMIN)

    @property
    def is_pupil(self):
        return self.check_role(UserRoles.PUPIL)

    @property
    def is_teacher(self):
        return self.check_role(UserRoles.TEACHER)


