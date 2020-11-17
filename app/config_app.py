import datetime


class DataBaseConfig:
    host = "localhost"
    port = "5432"
    login = 'code.cleverS_account'
    password = 'He24X4hI6bTL'
    db_name = "code.cleverS"

    conn_str = f'postgresql+psycopg2://{login}:{password}@{host}:{port}/{db_name}'


class ReCaptchaConfig:
    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = "6LevatQZAAAAAJDEMgq9cWVnSesRDTzAf_8MYBPE"
    RECAPTCHA_SECRET_KEY = "6LevatQZAAAAAJ7CUK3i1Hif-rPr_a1Le8oziuoN"


class MailConfig:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "goprog.clevers@gmail.com"
    MAIL_PASSWORD = "0efe5eb4d94b5d55"
    MAIL_DEFAULT_SENDER = "noreply@goprog.kz"


class SecretData:
    SECRET_KEY = "d7d2b771de3f6567cd3a4db4eb6751f2"


class StaticConfig:
    STATIC_FILES_VERSION = 3


class DefaultAdminConfig:
    ADMIN_DEFAULT_EMAIL = "admin@admin.com"  # После первого захода рекомендуется сменить
    ADMIN_DEFAULT_PASSWORD = "adminadmin"  # После первого захода рекомендуется сменить


class CheckerConfig:
    DOMAIN = "https://goprog.kz"

    CHECKER_HOST = 'http://178.159.39.154'
    BATCH_SUBS_URL = CHECKER_HOST + '/submissions/batch'

    API_TOKEN = 'bbb1db97e156ae820590702990b2a469'
    SECRET_KEY = 'dbf038cbd0aa97acbf7e92de8c7aff96'

    CALLBACK_ADDRESS = '/submission_result'
    CALLBACK_URL = DOMAIN + CALLBACK_ADDRESS

    CPU_TIME_LIMIT_MAX = 5
    MEMORY_LIMIT_MAX_MB = 1024

    HEADERS = {'X-Auth-Token': API_TOKEN}


class BaseConfig(SecretData, StaticConfig, ReCaptchaConfig, MailConfig, CheckerConfig, DefaultAdminConfig):
    DEBUG = False
    TESTING = False

    HOST = "localhost"
    PORT = "8080"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
