import datetime


class BaseConfig:
    SECRET_KEY = "d7d2b771de3f6567cd3a4db4eb6751f2"
    DEBUG = False
    TESTING = False
    HOST = "localhost"
    PORT = "8080"
    ADMIN_DEFAULT_EMAIL = "admin@admin.com"  # После первого захода рекомендуется сменить
    ADMIN_DEFAULT_PASSWORD = "backdoorisnotavailable"  # После первого захода рекомендуется сменить


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
