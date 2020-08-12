from .db_session import SqlAlchemyBase
import sqlalchemy


class Topic(SqlAlchemyBase):
    __tablename__ = "topics"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))


class TopicAvailable(SqlAlchemyBase):
    __tablename__ = "topic_available"

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
