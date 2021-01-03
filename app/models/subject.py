from .db_session import SqlAlchemyBase
from .db_helper import DbHelper
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Subject(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "subjects"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), unique=True)

    groups = orm.relationship("Group", back_populates="subject")
    teachers = orm.relationship("Teacher", secondary='teacher_to_subject', back_populates="subjects")

    def __eq__(self, other):
        return self.id == other.id