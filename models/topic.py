from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

topic_available = sqlalchemy.Table('group_to_topic', SqlAlchemyBase.metadata,
                                   sqlalchemy.Column('topic_id', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey("topics.id")),
                                   sqlalchemy.Column('group_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
                                   )


class Topic(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('lessons_count', 'groups_id', '-teacher', '-groups')
    __tablename__ = "topics"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), unique=True)

    author_teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))

    teacher = orm.relationship("Teacher", back_populates='topics')
    groups = orm.relationship('Group', secondary='group_to_topic', back_populates='topics', lazy='joined')
    lessons = orm.relationship("Lesson", back_populates='topic')

    @property
    def lessons_count(self):
        return len(self.lessons)

    @property
    def groups_id(self):
        return [group.id for group in self.groups]

