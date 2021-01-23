from sqlalchemy import func, distinct, and_, literal

from app.models import db_session
from app.models.group import Group
from app.models.lesson import Lesson
from app.models.task import Task, Solution, TaskCheckStatus
from app.models.course import Course
from app.models.pupil import Pupil


def tasks_count_of_pupil_for_course(*, pupil_id,
                                    solution_status=TaskCheckStatus.ACCESS):
    session = db_session.create_session()

    query = session \
        .query(Group.id,
               Course.id,
               Group.name,
               Course.name,
               func.count(distinct(Task.id)),
               literal(solution_status)) \
        .select_from(Pupil).filter(Pupil.id == pupil_id) \
        .join(Pupil.groups) \
        .join(Group.courses) \
        .join(Lesson, Lesson.course_id == Course.id) \
        .join(Task, Task.lesson_id == Lesson.id) \
        .outerjoin(Solution,
                   and_(Solution.task_id == Task.id,
                        Solution.pupil_id == pupil_id,
                        Solution.group_id == Group.id))

    if solution_status is TaskCheckStatus.ACCESS:
        query = query.filter(Solution.review_status.is_(TaskCheckStatus.ACCESS))
    else:
        query = query.filter(Solution.review_status.isnot(TaskCheckStatus.ACCESS))

    query = query\
        .group_by(Group.id, Course.id) \
        .order_by(Group.id, Course.id)

    return query.all()


def count_tasks_solved_for_lessons_by_pupil(*, pupil_id, group_id):
    session = db_session.create_session()
    query = session \
        .query(Lesson.id,
               func.count(distinct(Task.id))) \
        .select_from(Pupil) \
        .filter(Pupil.id == pupil_id) \
        .join(Group, Group.id == group_id) \
        .join(Group.lessons) \
        .join(Lesson.tasks) \
        .join(Solution, and_(Solution.pupil_id == pupil_id, Solution.group_id == group_id,
                             Solution.task_id == Task.id,
                             Solution.review_status.is_(TaskCheckStatus.ACCESS)))\
        .group_by(Lesson.id)
    return query.all()


def count_tasks_in_each_lesson_available_for_group(*, group_id):
    session = db_session.create_session()

    query = session \
        .query(Lesson.id,
               func.count(Task.id)) \
        .select_from(Group).filter(Group.id == group_id) \
        .join(Group.lessons) \
        .join(Lesson.tasks) \
        .group_by(Lesson.id)

    return query.all()


def count_tasks_solved_for_lessons_by_pupils_in_group(*, group_id):
    session = db_session.create_session()
    query = session \
        .query(Lesson.id,
               Task.id,
               func.count(distinct(Solution.pupil_id))) \
        .select_from(Group) \
        .join(Group.lessons) \
        .join(Lesson.tasks) \
        .join(Solution, and_(Solution.group_id == group_id, Solution.task_id == Task.id,
                             Solution.review_status.is_(TaskCheckStatus.ACCESS))) \
        .order_by(Lesson.id) \
        .group_by(Lesson.id, Task.id)
    return query.all()
