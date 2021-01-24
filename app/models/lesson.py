from .db_session import SqlAlchemyBase
from .db_helper import DbHelper

from datetime import timedelta
import sqlalchemy

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Lesson(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "lessons"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    html = sqlalchemy.Column(sqlalchemy.Text, default='')

    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courses.id", ondelete='CASCADE'))

    course = orm.relationship("Course", back_populates="lessons",
                              lazy='select')
    tasks = orm.relationship("Task", back_populates='lesson', cascade='all, delete-orphan', single_parent=True,
                             lazy='select')
    groups = orm.relationship('Group', secondary='lesson_to_group', back_populates='lessons',
                              lazy='select')

    def __eq__(self, other):
        return self.id == other.id


class LessonAvailableToGroup(SqlAlchemyBase):
    __tablename__ = 'lesson_to_group'

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("lessons.id", ondelete='CASCADE'),
                                  primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id", ondelete='CASCADE'),
                                 primary_key=True)

    available_from = sqlalchemy.Column(sqlalchemy.DateTime)
    seconds_to_deadline = sqlalchemy.Column(sqlalchemy.Integer)

    @property
    def deadline(self):
        if self.available_from and self.seconds_to_deadline:
            return self.available_from + timedelta(seconds=self.seconds_to_deadline)
