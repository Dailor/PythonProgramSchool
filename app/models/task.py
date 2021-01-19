from .db_session import SqlAlchemyBase
from .db_helper import DbHelper

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql
from sqlalchemy_serializer import SerializerMixin

import datetime


class ProgrammingLanguage:
    PYTHON = ('Python', 71)
    CPP = ('C++', 54)

    ALL = [PYTHON, CPP]


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


class ApiCheckAnswers:
    IN_QUEUE = 1
    ACCEPT = 3
    WRONG = 4


class TaskInfoFields:
    ACCEPT = 'accept'
    FAILED = 'failed'
    COUNT = 'count_all'


class Task(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(30))
    language_id = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.Text)
    solutions = sqlalchemy.Column(sqlalchemy.Text)

    time_sec = sqlalchemy.Column(sqlalchemy.Float, default=1)
    memory_mb = sqlalchemy.Column(sqlalchemy.Integer, default=16)
    tries_count = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    examples = sqlalchemy.Column(postgresql.ARRAY(sqlalchemy.JSON))
    examples_hidden = sqlalchemy.Column(postgresql.ARRAY(sqlalchemy.JSON))

    api_check = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id", ondelete='CASCADE'),
                                  nullable=False)

    lesson = orm.relationship("Lesson", back_populates='tasks')

    def get_tests_count(self):
        return len(self.examples) + len(self.examples_hidden)

    def __eq__(self, other):
        return self.id == other.id


class Solution(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = 'solutions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pupil_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('pupils.id', ondelete='CASCADE'),
                                 nullable=False)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', ondelete='CASCADE'),
                                 nullable=False)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id', ondelete='CASCADE'),
                                nullable=False)

    solution_info = sqlalchemy.Column(sqlalchemy.JSON)

    result = sqlalchemy.Column(sqlalchemy.Text)
    review_status = sqlalchemy.Column(sqlalchemy.Boolean)
    date_delivery = sqlalchemy.Column(sqlalchemy.DateTime(), default=datetime.datetime.utcnow)

    pupil = orm.relationship("Pupil", back_populates='solutions', lazy='joined')
    group = orm.relationship("Group", back_populates='solutions', lazy='joined')
    task = orm.relationship("Task")
    submissions_batch = orm.relationship("SubmissionsBatch", back_populates='solution', passive_deletes=True)

    def __eq__(self, other):
        return self.id == other.id
