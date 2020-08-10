import pytest
from app import bcrypt


def login(client, username="JohnDoe", password="password"):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def test_login(app_tester):
    # should redirect to login page
    response = app_tester.get("/")
    assert response.status_code == 302


def test_user_login(app_tester, init_database):
    # response = app_tester.post(
    #     "/login",
    #     data=dict(username="JohnDoe", password="password"),
    #     follow_redirects=True,
    # )
    response = login(app_tester)
    assert response.status_code == 200
    assert b"Pass on a message!" in response.data
    assert b"Lunch Times" in response.data


def test_incorrect_user_login(app_tester, init_database):
    response = login(app_tester, username="JaneLong", password="password")
    assert response.status_code == 200
    assert b"Login Unsuccessful" in response.data


def test_notication(app_tester, init_database):
    """
    test that a given user JohnDoe emits a notifications to all users except himself
    """
    pass


def test_profile_update(app_tester, init_database):
    """
    GIVEN a verified user
    WHEN user modifies profile
    THEN check that new preferences are saved
    """
    login(app_tester, username="JaneLong", password="differentpassword")
    response = app_tester.get("/profile")

    # check email fields
    assert b"Email" in response.data
    assert b"jane_long@gmail.com" in response.data

    # check phone fields
    assert b"Phone number" in response.data
    assert b"jane's phone" in response.data

    # now change the data
    changing_response = app_tester.post(
        "/profile",
        data={
            "email": "jane_long2@gmail.com",
            "phone": "new_phone",
            "preferred": "email",
        },
    )

    assert b"Email" in changing_response.data
    assert b"jane_long2@gmail.com" in changing_response.data

    # check phone fields
    assert b"Phone number" in changing_response.data
    assert b"new_phone" in changing_response.data


def test_email_connection(app_tester, init_database):
    """
    test whether an email was sent after creation of a time
    """
    from app import mail

    with mail.record_messages() as outbox:
        login(app_tester)
        app_tester.post(
            "/lunchbuddy",
            data=dict(message="Hello", time_out="12:30", time_back_in="13:30"),
        )
        assert len(outbox) == 1
        assert (
            outbox[0].subject == "New Lunch Time created."
        )  # will be the f-string of message
