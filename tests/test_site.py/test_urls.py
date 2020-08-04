import pytest
from app import bcrypt


def test_login(app_tester):
    # should redirect to login page
    response = app_tester.get("/")
    assert response.status_code == 302


def test_user_login(app_tester, init_database):
    response = app_tester.post(
        "/login",
        data=dict(username="JohnDoe", password="password"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Pass on a message!" in response.data
    assert b"Lunch Times" in response.data


def test_incorrect_user_login(app_tester, init_database):
    response = app_tester.post(
        "/login",
        data=dict(username="JaneLong", password="password"),
        follow_redirects=True,
    )
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
    # check email update
    # check phone update
    # check preference update
    response = app_tester.post(
        "/login",
        data=dict(username="JaneLong", password="password"),
        follow_redirects=True,
    )

