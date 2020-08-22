from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Teacher(SqlAlchemyBase):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), unique=True)

    user = orm.relationship("User", back_populates="teacher")
    subjects = orm.relationship("TeacherTeachesSubject", back_populates="teacher")
    groups = orm.relationship("Group", back_populates="teacher", lazy='joined')

    def get_string_groups(self):
        return [gr.name for gr in self.groups]

    def get_string_subjects(self):
        return [subject.name for subject in self.subjects]
