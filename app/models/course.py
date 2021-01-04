from .db_session import SqlAlchemyBase
from .db_helper import DbHelper
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Course(SqlAlchemyBase, SerializerMixin, DbHelper):
    __tablename__ = "courses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(30))

    curators = orm.relationship("Teacher", secondary='course_to_teacher', back_populates='courses')
    groups = orm.relationship('Group', secondary='course_to_group', back_populates='courses', lazy='joined')
    lessons = orm.relationship("Lesson", back_populates='course', order_by="Lesson.id.desc()",
                               cascade="all, delete",
                               passive_deletes=True)

    def is_curator(self, teacher):
        return any(teacher.id == curator.id for curator in self.curators)

    def lessons_count(self):
        return len(self.lessons)

    def groups_id(self):
        return [group.id for group in self.groups]

    def curators_id(self):
        curators = [curator.id for curator in self.curators]
        return curators if len(curators) else []

    def __eq__(self, other):
        return self.id == other.id


class CourseAvailable(SqlAlchemyBase):
    __tablename__ = 'course_to_group'
    course_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("courses.id", ondelete='CASCADE'), primary_key=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id", ondelete='CASCADE'), primary_key=True)


class CourseCurators(SqlAlchemyBase):
    __tablename__ = 'course_to_teacher'

    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('courses.id', ondelete="CASCADE"),
                                  primary_key=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id', ondelete='CASCADE'),
                                   primary_key=True)
