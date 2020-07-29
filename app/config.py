import os


class Configuration:

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Configuration_tester:

    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site_test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
