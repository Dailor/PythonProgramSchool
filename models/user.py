import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    username = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False, index=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    about_user = sqlalchemy.Column(sqlalchemy.String, default="Soon here will be information about me.")
