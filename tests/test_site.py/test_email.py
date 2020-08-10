import pytest


def test_email_connection(app_tester, init_database):
    """
    test whether an email was sent after creation of a time
    """
    with mail.record_messages() as outbox:
        

    pass
