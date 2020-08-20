from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    html = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    tasks = orm.relationship("Task")
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))


class LessonAvailable(SqlAlchemyBase):
    __tablename__ = "lesson_available"

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"), primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"), primary_key=True)

    group = orm.relationship("Group")
