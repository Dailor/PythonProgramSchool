from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Topic(SqlAlchemyBase):
    __tablename__ = "topics"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), unique=True)

    author_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    lessons = orm.relationship("Lesson")


class TopicAvailable(SqlAlchemyBase):
    __tablename__ = "topic_available"

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"), primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"), primary_key=True)

    group = orm.relationship("Group")