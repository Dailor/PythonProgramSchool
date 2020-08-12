from .db_session import SqlAlchemyBase
import sqlalchemy


class Teacher(SqlAlchemyBase):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"))

