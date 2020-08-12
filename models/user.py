import sqlalchemy
from enum import Enum
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class RolesEnum(Enum):
    ADMIN = "admin"
    PUPIL = "pupil"
    TEACHER = "teacher"


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    email = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False, index=True, unique=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    about_user = sqlalchemy.Column(sqlalchemy.String, default="Soon here will be information about me.")


class Roles(SqlAlchemyBase):
    __tablename__ = "roles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
