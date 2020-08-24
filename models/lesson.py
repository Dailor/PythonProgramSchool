from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy

lesson_available = sqlalchemy.Table('lesson_to_group', SqlAlchemyBase.metadata,
                                    sqlalchemy.Column('lesson_id', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey("lessons.id"),
                                                      primary_key=True),
                                    sqlalchemy.Column('group_id', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey("groups.id"),
                                                      primary_key=True)
                                    )


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    html = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))

    tasks = orm.relationship("Task")
    groups = orm.relationship('Group', secondary='lesson_to_group', back_populates='lessons')
