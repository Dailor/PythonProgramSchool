from .db_session import SqlAlchemyBase
import sqlalchemy


class Subject(SqlAlchemyBase):
    __tablename__ = "subjects"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
