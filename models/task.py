from .db_session import SqlAlchemyBase

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

import datetime

class TaskCheckMethods:
    MANUAL_CHECK = "manual_check"


class TaskCheckStatus:
    ACCESS = True
    WAITING = None
    FAILED = False

    ALL_STATUS = ACCESS, WAITING, FAILED


class TaskCheckStatusString:
    ACCESS = "solved"
    FAILED = 'failed'
    WAITING = 'waiting'
    NOT_PASS = 'not pass'

    ALL_STATUS = ACCESS, WAITING, FAILED, NOT_PASS


class Task(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ("-lesson",)

    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(30))
    description = sqlalchemy.Column(sqlalchemy.Text)
    in_data = sqlalchemy.Column(sqlalchemy.Text)
    out_data = sqlalchemy.Column(sqlalchemy.Text)

    type_check = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"))

    lesson = orm.relationship("Lesson", back_populates='tasks')


class Solutions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'solutions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pupil_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('pupils.id'),
                                 nullable=False)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'),
                                 nullable=False)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id'),
                                nullable=False)

    result = sqlalchemy.Column(sqlalchemy.Text)
    review_status = sqlalchemy.Column(sqlalchemy.Boolean)
    date_delivery = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)

    pupil = orm.relationship("Pupil", back_populates='solutions', lazy='joined')
    group = orm.relationship("Group", back_populates='solutions', lazy='joined')
    task = orm.relationship("Task")

