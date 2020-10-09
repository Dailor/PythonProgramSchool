from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy


class Pupil(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('-solutions', "groups_id", 'groups')
    __tablename__ = "pupils"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), unique=True)

    user = orm.relationship("User", back_populates="pupil")
    groups = orm.relationship("Group", secondary='pupils_to_groups', back_populates="pupils", lazy='joined')
    solutions = orm.relationship("Solutions", back_populates='pupil')

    @property
    def groups_id(self):
        return [group.id for group in self.groups]
