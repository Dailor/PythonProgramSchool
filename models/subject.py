from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Subject(SqlAlchemyBase):
    __tablename__ = "subjects"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), unique=True)

    groups = orm.relationship("Group", back_populates="subject")
    teachers = orm.relationship("TeacherTeachesSubject", back_populates="subject")


class TeacherTeachesSubject(SqlAlchemyBase):
    __tablename__ = "teacher_teaches_subject"

    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), primary_key=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"), primary_key=True)

    teacher = orm.relationship("Teacher", back_populates="subjects")
    subject = orm.relationship("Subject", back_populates="teachers")
