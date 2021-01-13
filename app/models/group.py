from .db_session import SqlAlchemyBase, create_session
from .db_helper import DbHelper

from flask_restful import abort

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
import sqlalchemy

import os

pupils_groups = sqlalchemy.Table('pupils_to_groups', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('pupil_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey("pupils.id", ondelete='CASCADE'),
                                                   primary_key=True),
                                 sqlalchemy.Column('group_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey("groups.id", ondelete='CASCADE'),
                                                   primary_key=True))


class Group(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "groups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), unique=True, nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    invite_code = sqlalchemy.Column(sqlalchemy.String(255), unique=True, nullable=False)

    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id", ondelete="SET NULL"))

    teacher = orm.relationship("Teacher", back_populates="groups", lazy='joined')
    pupils = orm.relationship("Pupil", secondary='pupils_to_groups', back_populates="groups", lazy='select')

    courses = orm.relationship("Course", secondary='course_to_group', back_populates='groups', lazy='select',
                               order_by="Course.id")
    lessons = orm.relationship("Lesson", secondary='lesson_to_group', back_populates='groups', lazy='select',
                               order_by="Lesson.course_id, Lesson.id.desc()")
    solutions = orm.relationship("Solution", back_populates='group', lazy='select',
                                 cascade="all, delete",
                                 passive_deletes=True)

    def get_lesson_available_by_lesson(self, lesson):
        for lesson_available in self.lessons:
            if lesson_available.id == lesson.id:
                return lesson_available

    def courses_id(self):
        return [course.id for course in self.courses]

    def __eq__(self, other):
        return self.id == other.id

    def generate_invite_code(self):
        self.invite_code = os.urandom(64).hex()

    def is_have_permission(self, user):
        if not (user.is_admin or self.teacher_id == user.teacher.id):
            return abort(403)

    @staticmethod
    def get_by_invite_code(invite_code):
        session = create_session()
        group = session.query(Group).filter(Group.invite_code == invite_code).first()

        if group is None:
            return abort(403)

        return group

    def all_lessons(self):
        return [lesson for course in self.courses for lesson in course.lessons]
