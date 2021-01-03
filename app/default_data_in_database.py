from app.models import db_session
from app.models.__all_models import User, Admin, ContestSystemsAvailable, ContestSystem
from app.config_app import DefaultAdminConfig


def __admin():
    session = db_session.create_session()
    user = session.query(User).get(DefaultAdminConfig.ADMIN_DEFAULT_ID)

    if user:
        return

    user = User()
    user.id = DefaultAdminConfig.ADMIN_DEFAULT_ID
    user.name = DefaultAdminConfig.ADMIN_NAME
    user.surname = DefaultAdminConfig.ADMIN_SURNAME
    user.email = DefaultAdminConfig.ADMIN_DEFAULT_EMAIL
    user.set_password(DefaultAdminConfig.ADMIN_DEFAULT_PASSWORD)

    admin_user = Admin()
    user.admin = admin_user

    session.add(user)
    session.commit()


def __contest_system():
    session = db_session.create_session()

    in_db_services = {service.id: True for service in session.query(ContestSystem).all()}

    contest_system_not_exist = filter(lambda contest_system: contest_system.value not in in_db_services,
                                      ContestSystemsAvailable._value_to_instance_map.values())

    for contest_system_enum in contest_system_not_exist:
        contest_system = ContestSystem()
        contest_system.id = contest_system_enum.id
        contest_system.name = contest_system_enum.text
        session.add(contest_system)

    session.commit()


def add_default_data():
    __admin()
    __contest_system()


add_default_data()
