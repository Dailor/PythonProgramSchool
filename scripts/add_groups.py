from app.models import db_session
from app.models.__all_models import User, Teacher, Group, Pupil
import json
import os

filename = 'groups.json'


def get_data():
    with open(filename) as f:
        data = json.load(f)
    return data


def teacher_fullname(name, surname):
    user = User()
    user.name = name
    user.surname = surname

    return user.full_name

def add_groups():
    db_session.global_init(debug=True)

    session = db_session.create_session()

    data = get_data()

    teachers_dict = dict()

    for teacher_id, teacher_dict in enumerate(data['teachers']):
        user = User()

        user.name = teacher_dict['name']
        user.surname = teacher_dict['surname']
        user.email = teacher_dict['email']

        user.set_password(teacher_dict['password'])

        teacher = Teacher()
        user.teacher = teacher

        teachers_dict[user.full_name] = teacher

        session.add(user)

    for group_dict in data['groups']:
        group = Group()
        group.name = group_dict['name']
        group.generate_invite_code()

        teacher_name, teacher_surname = group_dict['teacher']['name'], group_dict['teacher']['surname']

        teacher = teachers_dict[teacher_fullname(teacher_name, teacher_surname)]
        group.teacher = teacher

        for pupil_dict in group_dict['pupils']:
            user = User()

            user.name = pupil_dict['name']
            user.surname = pupil_dict['surname']
            user.email = pupil_dict['email']

            user.set_password(pupil_dict['password'])

            pupil = Pupil()
            user.pupil = pupil

            group.pupils.append(pupil)
            session.add(group)

    session.commit()


if __name__ == '__main__':
    add_groups()
