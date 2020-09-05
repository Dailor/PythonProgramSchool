from models import db_session

from models.pupil import Pupil
from models.topic import Topic
from models.task import Task, Solutions, TaskCheckStatus
from models.group import Group
from models.lesson import Lesson

from sqlalchemy import func, distinct, and_, literal


def tasks_count_of_pupils_for_topic(*, pupil_id=None,
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


def tasks_solved_all_pupils_in_group_of_lesson(*, group_id):
    session = db_session.create_session()
    query = session.query(Lesson.id, Lesson.name, func.count(Solutions.id)).select_from(Group)
    query = query.join(Group.solutions)
    query = query.join(Lesson, Lesson.id, Solutions.lesson_id == Lesson.id)
    query = query.filter(Solutions.group_id == group_id,
                         Solutions.review_status == TaskCheckStatus.ACCESS)
    query = query.order_by(Lesson.id)
    query = query.group_by(Lesson.id)
    return query.all()
