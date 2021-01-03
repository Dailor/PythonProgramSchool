from flask_restful import abort
from .db_session import create_session


class DbHelper:
    NOT_FOUND_MSG = "{} с {} id не найдено"

    @classmethod
    def get_entity_or_404(cls, entity_id):
        session = create_session()
        entity = session.query(cls).get(entity_id)

        if entity is None:
            return abort(404, message=cls.NOT_FOUND_MSG.format(cls.__name__, entity_id))
        return entity
