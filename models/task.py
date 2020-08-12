from .db_session import SqlAlchemyBase
from enum import Enum
import sqlalchemy


class TaskCheck(Enum):
    MANUAL_CHECK = "manual_check"


class Task(SqlAlchemyBase):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    type_check = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"))
