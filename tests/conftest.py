import pytest
from app import create_app, db, bcrypt
from app.config import Configuration_tester
from app.models import Employee, LunchTime
from datetime import datetime


# @pytest.fixture(scope="module")
# def baseQuery():
#     return Employee.query.all()


@pytest.fixture(scope="module")
def app_tester():
    app = create_app(Configuration_tester)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture()
def init_database(scope="module"):
    db.create_all()

    emp1 = Employee(
        username="JohnDoe",
        password=bcrypt.generate_password_hash("password"),
        email="john_doe@gmail.com",
        phone_number="john's phone",
        preferred="phone",
    )
    emp2 = Employee(
        username="JaneLong",
        password=bcrypt.generate_password_hash("differentpassword"),
        email="jane_long@gmail.com",
        phone_number="jane's phone",
        preferred="email",
    )

    lunchtime1 = LunchTime(
        timeIn=datetime(2020, 7, 15, 12, 30),
        timeOut=datetime(2020, 7, 15, 11, 30),
        employee_id=1,  # JohnDoe should be employee # 1
    )
    lunchtime2 = LunchTime(
        timeIn=datetime(2020, 7, 15, 13, 30),
        timeOut=datetime(2020, 7, 15, 12, 30),
        employee_id=2,  # JaneLong should be employee # 2
    )

    db.session.add(emp1)
    db.session.add(emp2)
    db.session.add(lunchtime1)
    db.session.add(lunchtime2)
    db.session.commit()

    yield db

    db.drop_all()

