from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Teacher(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('-groups', 'name')
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), unique=True)

    user = orm.relationship("User", back_populates="teacher")
    subjects = orm.relationship("Subject", secondary='teacher_to_subject', back_populates="teachers")
    groups = orm.relationship("Group", back_populates="teacher", lazy='joined')
    topics = orm.relationship("Topic", back_populates='teacher', lazy='joined')

    def get_string_groups(self):
        return [gr.name for gr in self.groups]

    def get_string_subjects(self):
        return [subject.name for subject in self.subjects]

    @property
    def name(self):
        return self.user.full_name
