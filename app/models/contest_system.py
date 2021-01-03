from .db_helper import DbHelper
from .db_session import SqlAlchemyBase

from fast_enum import FastEnum
from sqlalchemy import orm

import sqlalchemy


class ContestSystemsAvailable(metaclass=FastEnum):
    __slots__ = ('id', 'text', 'submissions_history_url')

    CODEFORCE = 0, 'Codeforces', 'https://codeforces.com/submissions/'
    ACMP = 1, "ACMP", "https://acmp.ru/index.asp?main=status&id_mem="

    def __init__(self, value, text, last_submissions_url, name):
        self.name = name
        self.value = value
        self.id = value
        self.text = text
        self.submissions_history_url = last_submissions_url


class ContestSystem(SqlAlchemyBase, DbHelper):
    __tablename__ = 'contest_systems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255))

    contest_system_to_pupils = orm.relationship('ContestSystemToPupil', cascade='all, delete', passive_deletes=True)


class ContestSystemToPupil(SqlAlchemyBase):
    __tablename__ = 'contest_system_to_pupil'

    pupil_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('pupils.id', ondelete='CASCADE'),
                                 primary_key=True, nullable=False)
    contest_system_id = sqlalchemy.Column(sqlalchemy.Integer,
                                          sqlalchemy.ForeignKey('contest_systems.id', ondelete='CASCADE'),
                                          primary_key=True, nullable=False)
    id_on_contest_system = sqlalchemy.Column(sqlalchemy.String(200))

    contest_system = orm.relationship('ContestSystem', lazy='joined')
    pupil = orm.relationship('Pupil')

    @property
    def url_to_submissions_history_url(self):
        if self.id_on_contest_system:
            return ContestSystemsAvailable._value_to_instance_map[
                       self.contest_system_id].submissions_history_url + self.id_on_contest_system
