import os

all_teachers = set()

user_id_unique = os.urandom(2).hex()
user_id_now = 0

password_len = 6


class User:
    name = None
    surname = None
    password = None
    email = None

    def __init__(self, surname, name):
        self.surname = surname
        self.name = name
        self.generate_password()
        self.generate_email()

    def generate_password(self):
        self.password = os.urandom(password_len // 2).hex()

    def generate_email(self):
        global user_id_now
        user_id_now += 1

        self.email = f"user{user_id_now}_{user_id_unique}@fizmat.com"

    def serialize(self):
        return {'name': self.name,
                'surname': self.surname,
                'email': self.email,
                'password': self.password}


class Group:
    _teacher = None

    def __init__(self, class_name, group_no):
        self.name = f"Класс {class_name}, {group_no} группа "
        self.pupils = list()

    def serialize(self):
        return {
            'name': self.name,
            'teacher': self.teacher.serialize(),
            'pupils': [pupil.serialize() for pupil in self.pupils]
        }

    @staticmethod
    def serialize_groups(groups):
        return {'groups': [group.serialize() for group in groups]}

    def append(self, pupil):
        pupil.group_set = True
        self.pupils.append(pupil)

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, teacher):
        global all_teachers
        all_teachers.add(teacher)

        self._teacher = teacher


class Teacher(User):
    def __eq__(self, other):
        return self.name == other.name and self.surname == other.surname

    def __hash__(self):
        return hash(self.name + self.surname)

    @staticmethod
    def get_all_teachers():
        global all_teachers
        return all_teachers


class Pupil(User):
    name = None
    surname = None
    group_set = False
    class_name = None

    def serialize(self):
        result = super().serialize()

        if self.class_name:
            result['class_name'] = self.class_name

        return result
