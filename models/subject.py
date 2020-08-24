from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

teacher_teaches_subject = sqlalchemy.Table('teacher_to_subject', SqlAlchemyBase.metadata,
                                           sqlalchemy.Column('teacher_id', sqlalchemy.Integer,
                                                             sqlalchemy.ForeignKey("teachers.id")),
                                           sqlalchemy.Column('subject_id', sqlalchemy.Integer,
                                                             sqlalchemy.ForeignKey("subjects.id"))
                                           )


class Subject(SqlAlchemyBase, SerializerMixin):
    serialize_rules = ('-groups', '-teachers')
    __tablename__ = "subjects"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), unique=True)

    groups = orm.relationship("Group", back_populates="subject")
    teachers = orm.relationship("Teacher", secondary='teacher_to_subject', back_populates="subjects")
