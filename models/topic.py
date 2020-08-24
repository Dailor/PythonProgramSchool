from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm

topic_available = sqlalchemy.Table('group_to_topic', SqlAlchemyBase.metadata,
                                   sqlalchemy.Column('topic_id', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey("topics.id")),
                                   sqlalchemy.Column('group_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
                                   )


class Topic(SqlAlchemyBase):
    __tablename__ = "topics"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), unique=True)

    author_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    groups = orm.relationship('Group', secondary='group_to_topic', back_populates='topics')
    lessons = orm.relationship("Lesson")
