import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(debug):
    global __factory

    if __factory:
        return

    # При изменений параметров которые изменять conn_str, нужно зайти PythonProgramSchool/alembic.ini и поменять там ссылку
    _host = "localhost"  # Если приложение станет высоконагруженным, базу надо будет держать на другом сервере
    _port = "3307"  # Желательно дефолтный поменять
    _login = 'postgres'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    _password = 'root'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    _db_name = "python_school"  # Не забудьте создать базу с таким именем

    conn_str = f'postgresql+psycopg2://{_login}:{_password}@{_host}:{_port}/{_db_name}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=debug)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
