import pytest
from app import create_app, db, bcrypt
from app.config import Configuration_tester
from app.models import Employee


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
        username="JohnDoe", password=bcrypt.generate_password_hash("password")
    )
    emp2 = Employee(
        username="JaneLong", password=bcrypt.generate_password_hash("differentpassword")
    )

    db.session.add(emp1)
    db.session.add(emp2)

    db.session.commit()

    yield db

    db.drop_all()
