from sqlalchemy import func, distinct, and_, literal, exists, not_

from models import db_session
from models.group import Group
from models.lesson import Lesson
from models.task import Task, Solutions, TaskCheckStatus
from models.topic import Topic
from models.pupil import Pupil


def tasks_count_of_pupil_for_topic(*, pupil_id,
                                   solution_status=TaskCheckStatus.ACCESS):
    session = db_session.create_session()

    query = session.query(Group.id, Topic.id, Group.name, Topic.name, func.count(distinct(Task.id)),
                          literal(solution_status)).select_from(Group)
    query = query.join(Group.topics)
    query = query.join(Lesson, Lesson.topic_id == Topic.id)
    query = query.join(Task, Task.lesson_id == Lesson.id)
    query = query.outerjoin(Solutions,
                            and_(Solutions.task_id == Task.id,
                                 Solutions.pupil_id == pupil_id,
                                 Solutions.group_id == Group.id))

    if solution_status is TaskCheckStatus.ACCESS:
        query = query.filter(Solutions.review_status.is_(TaskCheckStatus.ACCESS))
    else:
        query = query.filter(Solutions.review_status.isnot(TaskCheckStatus.ACCESS))

    query = query.group_by(Group.id, Topic.id)
    query = query.order_by(Group.id, Topic.id)

    return query.all()


def count_tasks_solved_for_lessons_by_pupil(*, pupil_id, group_id):
    session = db_session.create_session()
    query = session.query(Lesson.id, func.count(Task.id))
    query = query.select_from(Group).filter(Group.id == group_id)
    query = query.join(Group.lessons)
    query = query.join(Lesson.tasks)
    query = query.join(Solutions, and_(Solutions.pupil_id == pupil_id, Solutions.group_id == group_id,
                                       Solutions.task_id == Task.id,
                                       Solutions.review_status.is_(TaskCheckStatus.ACCESS)))
    query = query.group_by(Lesson.id)
    return query.all()


def count_tasks_in_each_lesson_available_for_group(*, group_id):
    session = db_session.create_session()

    query = session.query(Lesson.id, func.count(Task.id))
    query = query.select_from(Group).filter(Group.id == group_id)
    query = query.join(Group.lessons)
    query = query.join(Lesson.tasks)
    query = query.group_by(Lesson.id)

    return query.all()


def count_tasks_solved_for_lessons_by_pupils_in_group(*, group_id):
    session = db_session.create_session()
    query = session.query(Lesson.id, Task.id, func.count(Solutions.id)).select_from(Group)
    query = query.join(Group.lessons)
    query = query.join(Lesson.tasks)
    query = query.join(Solutions, and_(Solutions.group_id == group_id, Solutions.task_id == Task.id,
                                       Solutions.review_status.is_(TaskCheckStatus.ACCESS)))
    query = query.order_by(Lesson.id)
    query = query.group_by(Lesson.id, Task.id)
    return query.all()