from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
import sqlalchemy

pupils_groups = sqlalchemy.Table('pupils_to_groups', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('pupil_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("pupils.id"),
                                                   primary_key=True),
                                 sqlalchemy.Column('group_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"),
                                                   primary_key=True))


class Group(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('-pupils', '-topics', 'topics_list')

    __tablename__ = "groups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(20), unique=True, nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id", on_delete='SET NULL'))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id", on_delete='SET NULL'))

    subject = orm.relationship("Subject", uselist=False, back_populates="groups")
    teacher = orm.relationship("Teacher", uselist=False, back_populates="groups")
    pupils = orm.relationship("Pupil", secondary='pupils_to_groups', back_populates="groups")

    topics = orm.relationship("Topic", secondary='group_to_topic', back_populates='groups')
    lessons = orm.relationship("Lesson", secondary='lesson_to_group', back_populates='groups')

    @property
    def topics_list(self):
        return [topic.name for topic in self.topics]

