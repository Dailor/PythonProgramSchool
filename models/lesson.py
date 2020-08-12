from .db_session import SqlAlchemyBase
import sqlalchemy


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    html = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))


class TopicAvailable(SqlAlchemyBase):
    __tablename__ = "topic_available"

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
