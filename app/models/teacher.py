from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Teacher(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'), unique=True,
                                nullable=False)

    user = orm.relationship("User", back_populates="teacher", lazy='joined')
    groups = orm.relationship("Group", back_populates="teacher", lazy='joined')
    courses = orm.relationship("Course", secondary='course_to_teacher', back_populates='curators', lazy='select')

    def get_string_groups(self):
        return [gr.name for gr in self.groups]

    @property
    def name(self):
        return self.user.full_name

    def __eq__(self, other):
        return self.id == other.id
