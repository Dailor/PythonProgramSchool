from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy

lesson_available = sqlalchemy.Table('lesson_to_group', SqlAlchemyBase.metadata,
                                    sqlalchemy.Column('lesson_id', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey("lessons.id"),
                                                      primary_key=True),
                                    sqlalchemy.Column('group_id', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey("groups.id"),
                                                      primary_key=True)
                                    )


class Lesson(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('-topic_id', '-topic', '-groups')
    __tablename__ = "lessons"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    html = sqlalchemy.Column(sqlalchemy.Text, default='')

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))

    topic = orm.relationship("Topic", back_populates="lessons")
    tasks = orm.relationship("Task", back_populates='lesson')
    groups = orm.relationship('Group', secondary='lesson_to_group', back_populates='lessons')

    def __eq__(self, other):
        return self.id == other.id
