from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy


class Group(SqlAlchemyBase):
    __tablename__ = "groups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(20), unique=True, nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))

    subject = orm.relationship("Subject", uselist=False, back_populates="groups")
    teacher = orm.relationship("Teacher", uselist=False, back_populates="groups")
    pupils = orm.relationship("PupilsGroups", back_populates="group")

    topics_available = orm.relationship("TopicAvailable")
    lessons_available = orm.relationship("LessonAvailable")


class PupilsGroups(SqlAlchemyBase):
    __tablename__ = "pupils_group"

    pupil_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("pupils.id"), primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"), primary_key=True)

    pupil = orm.relationship("Pupil", back_populates="groups")
    group = orm.relationship("Group", back_populates="pupils")
