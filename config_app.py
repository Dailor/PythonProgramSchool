import datetime


class DataBaseConfig:
    host = "localhost"  # Если приложение станет высоконагруженным, базу надо будет держать на другом сервере
    port = "5432"  # Желательно дефолтный поменять
    login = 'code.cleverS_account'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    password = 'He24X4hI6bTL'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    db_name = "code.cleverS"  # Не забудьте создать базу с таким именем

    conn_str = f'postgresql+psycopg2://{login}:{password}@{host}:{port}/{db_name}'


class BaseConfig:
    SECRET_KEY = "d7d2b771de3f6567cd3a4db4eb6751f2"
    DEBUG = False
    TESTING = False
    HOST = "localhost"
    PORT = "8080"
    ADMIN_DEFAULT_EMAIL = "admin@admin.com"  # После первого захода рекомендуется сменить
    ADMIN_DEFAULT_PASSWORD = "adminadmin"  # После первого захода рекомендуется сменить


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
