import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


def check_models_on_equal(self, other):
    if not isinstance(other, self.__class__):
        return False
    return self.id == other.id


SqlAlchemyBase = dec.declarative_base()
SqlAlchemyBase.__eq__ = check_models_on_equal

__factory = None


def global_init(debug):
    global __factory

    if __factory:
        return

    from app.config_app import DataBaseConfig

    conn_str = DataBaseConfig.conn_str
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=debug, pool_size=50, max_overflow=0)
    __factory = orm.scoped_session(orm.sessionmaker(bind=engine))

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
