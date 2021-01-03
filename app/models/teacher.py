from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Teacher(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'), unique=True,
                                nullable=False)

    user = orm.relationship("User", back_populates="teacher")
    subjects = orm.relationship("Subject", secondary='teacher_to_subject', back_populates="teachers")
    groups = orm.relationship("Group", back_populates="teacher", lazy='joined')
    courses = orm.relationship("Course", secondary='course_to_teacher', back_populates='curators', lazy='joined')

    def get_string_groups(self):
        return [gr.name for gr in self.groups]

    def get_string_subjects(self):
        return [subject.name for subject in self.subjects]

    @property
    def name(self):
        return self.user.full_name

    def __eq__(self, other):
        return self.id == other.id

class TeacherTeachesSubjects(SqlAlchemyBase):
    __tablename__ = 'teacher_to_subject'

    teacher_id = sqlalchemy.Column('teacher_id', sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True)
    subject_id = sqlalchemy.Column('subject_id', sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)
