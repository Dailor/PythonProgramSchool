def set_global_jinja_variables(app):
    from app.utils import time

    @app.context_processor
    def context_processor():
        return dict(STATIC_FILES_VERSION=app.config['STATIC_FILES_VERSION'],
                    get_utc_date_in_iso=time.get_utc_date_in_iso)
