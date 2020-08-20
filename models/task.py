from .db_session import SqlAlchemyBase
import sqlalchemy


class TaskCheckMethods:
    MANUAL_CHECK = "manual_check"


class Task(SqlAlchemyBase):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30))
    type_check = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"))
