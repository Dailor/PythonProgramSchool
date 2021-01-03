from .db_session import SqlAlchemyBase, create_session
from .db_helper import DbHelper
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy


class Pupil(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "pupils"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id", ondelete='CASCADE'), unique=True)

    user = orm.relationship("User", back_populates="pupil")
    groups = orm.relationship("Group", secondary='pupils_to_groups', back_populates="pupils", lazy='joined')
    solutions = orm.relationship("Solution", back_populates='pupil', cascade="all, delete",
                                 passive_deletes=True)
    contest_systems = orm.relationship('ContestSystemToPupil', cascade='all, delete',
                                       passive_deletes=True)

    @property
    def groups_id(self):
        return [group.id for group in self.groups]

    def __eq__(self, other):
        return self.id == other.id

    def available_contest_systems(self):
        from .contest_system import ContestSystemsAvailable, ContestSystem, ContestSystemToPupil

        all_pupil_contest_systems = []

        for contest_system_id, contest_system in ContestSystemsAvailable._value_to_instance_map.items():
            flag = True

            for pupil_contest_system in self.contest_systems:
                if contest_system.value == pupil_contest_system.contest_system_id:
                    all_pupil_contest_systems.append(pupil_contest_system)
                    flag = False
                    break

            if flag:
                contest_system_need = ContestSystem()
                pupil_contest_system = ContestSystemToPupil()

                contest_system_need.id = contest_system.id
                contest_system_need.name = contest_system.text

                pupil_contest_system.contest_system = contest_system_need
                all_pupil_contest_systems.append(pupil_contest_system)

        return all_pupil_contest_systems
