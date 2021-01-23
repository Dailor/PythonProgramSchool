from .db_session import SqlAlchemyBase

import sqlalchemy

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Submission(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'submissions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    token_sub = sqlalchemy.Column(sqlalchemy.String)
    submissions_batch_id = sqlalchemy.Column(sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey('submissions_batch.id', ondelete='CASCADE'))

    stdout = sqlalchemy.Column(sqlalchemy.String)
    stderr = sqlalchemy.Column(sqlalchemy.String)

    status = sqlalchemy.Column(sqlalchemy.JSON)
    time = sqlalchemy.Column(sqlalchemy.Float)
    memory = sqlalchemy.Column(sqlalchemy.Float)

    submissions_batch = orm.relationship('SubmissionsBatch', back_populates='submissions', uselist=False)

    def __eq__(self, other):
        return self.id == other.id


class SubmissionsBatchStatistic:
    MAX_TIME_SEC = 'max_time'
    MAX_MEMORY_MB = 'max_memory'
    ERRORS = 'errors'
    PASSED = 'passed'
    FAILED = 'failed'
    COUNT = 'tests_count'


class SubmissionsBatch(SqlAlchemyBase):
    __tablename__ = 'submissions_batch'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    solution_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('solutions.id', ondelete='CASCADE'))

    accepted_tasks_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    failed_tasks_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    all_tasks_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    solution = orm.relationship("Solution", back_populates='submissions_batch')
    submissions = orm.relationship("Submission", back_populates='submissions_batch',
                                   cascade="all, delete",
                                   passive_deletes=True)

    def get_checked_count(self):
        return self.failed_tasks_count + self.accepted_tasks_count

    def get_statistic(self):
        if len(self.submissions) == 0:
            return dict()

        max_memory = self.submissions[0].memory
        max_time = self.submissions[0].time
        errors = set()

        for submission in self.submissions:
            if max_memory:
                max_memory = max(max_memory, submission.memory)
            else:
                max_memory = submission.memory

            if max_time:
                max_time = max(max_time, submission.time)
            else:
                max_time = submission.time

            status_id, status_text = submission.status['id'], submission.status['description']

            if status_id > 3:
                errors.add(status_text)

        if not max_memory:
            max_memory = 0
        if not max_time:
            max_time = 0

        return {SubmissionsBatchStatistic.MAX_TIME_SEC: max_time,
                SubmissionsBatchStatistic.MAX_MEMORY_MB: max_memory / 1000,
                SubmissionsBatchStatistic.ERRORS: ', '.join(errors),
                SubmissionsBatchStatistic.PASSED: self.accepted_tasks_count,
                SubmissionsBatchStatistic.FAILED: self.failed_tasks_count,
                SubmissionsBatchStatistic.COUNT: self.all_tasks_count}

    def __eq__(self, other):
        return self.id == other.id
