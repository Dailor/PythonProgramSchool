from .db_session import SqlAlchemyBase
import sqlalchemy


class Task(SqlAlchemyBase):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)