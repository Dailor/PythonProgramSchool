import datetime

default_admin_login = "admin"
default_admin_password = "admin"

host = "localhost"
port = "8080"


def set_config(app):
    app.config.update(
        SECRET_KEY=b'q\x07\x18\xb8TE\xf4\xa8l\xe8\xfdX\xf1\xeaZ\xa4',
        PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=365)
    )

