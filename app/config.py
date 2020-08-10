import os


class Configuration:

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_DEFAULT_SENDER = "uthelpsinsurance@gmail.com"
    MAIL_USERNAME = "uthelpsinsurance@gmail.com"
    MAIL_PASSWORD = "Pinkfloyd2#"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class Configuration_tester:

    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site_test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_DEFAULT_SENDER = "uthelpsinsurance@gmail.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USERNAME = "uthelpsinsurance@gmail.com"
    MAIL_PASSWORD = "Pinkfloyd2#"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
