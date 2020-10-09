import datetime


class DataBaseConfig:
    host = "localhost"  # Если приложение станет высоконагруженным, базу надо будет держать на другом сервере
    port = "5432"  # Желательно дефолтный поменять
    login = 'code.cleverS_account'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    password = 'He24X4hI6bTL'  # НУЖНО ПОМЕНЯТЬ В БАЗЕ И ЗДЕСЬ
    db_name = "code.cleverS"  # Не забудьте создать базу с таким именем

    conn_str = f'postgresql+psycopg2://{login}:{password}@{host}:{port}/{db_name}'


class ReCaptchaConfig:
    RECAPTCHA_PUBLIC_KEY = "6LevatQZAAAAAJDEMgq9cWVnSesRDTzAf_8MYBPE"
    RECAPTCHA_PRIVATE_KEY = "6LevatQZAAAAAJ7CUK3i1Hif-rPr_a1Le8oziuoN"


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


class BaseConfig:
    SECRET_KEY = SecretData.SECRET_KEY

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = ReCaptchaConfig.RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_SECRET_KEY = ReCaptchaConfig.RECAPTCHA_PRIVATE_KEY

    MAIL_SERVER = MailConfig.MAIL_SERVER
    MAIL_PORT = MailConfig.MAIL_PORT
    MAIL_USE_TLS = MailConfig.MAIL_USE_TLS
    MAIL_USE_SSL = MailConfig.MAIL_USE_SSL
    MAIL_USERNAME = MailConfig.MAIL_USERNAME
    MAIL_PASSWORD = MailConfig.MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MailConfig.MAIL_DEFAULT_SENDER

    DEBUG = False
    TESTING = False

    HOST = "localhost"
    PORT = "8080"
    ADMIN_DEFAULT_EMAIL = "admin@admin.com"  # После первого захода рекомендуется сменить
    ADMIN_DEFAULT_PASSWORD = "adminadmin"  # После первого захода рекомендуется сменить


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
