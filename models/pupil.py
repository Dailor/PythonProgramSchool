from .db_session import SqlAlchemyBase
import sqlalchemy


class Pupil(SqlAlchemyBase):
    __tablename__ = "pupils"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))