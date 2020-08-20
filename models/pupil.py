from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy


class Pupil(SqlAlchemyBase):
    __tablename__ = "pupils"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), unique=True)

    user = orm.relationship("User")
    groups = orm.relationship("PupilsGroups", back_populates="pupil")
