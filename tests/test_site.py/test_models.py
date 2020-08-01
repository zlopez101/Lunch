import pytest
from app.models import Employee, LunchTime
from datetime import datetime


def test_Employee(app_tester, init_database):
    """
    GIVEN new employee
    WHEN employee is added
    THEN check employees can be added and deleted from database
    """

    emp2 = Employee(username="testing", password="password")
    init_database.session.add(emp2)
    init_database.session.commit()

    emps = Employee.query.all()
    assert len(emps) == 3
    assert emps[-1].username == "testing"

    init_database.session.delete(emp2)
    init_database.session.commit()

    emps = Employee.query.all()
    assert len(emps) == 2
    assert emps[-1].username == "JaneLong"


def test_LunchTime(app_tester, init_database):
    """
    GIVEN LunchTime
    WHEN a new LunchTime occurs
    THEN previous LunchTime should be deleted
    """
    lunches = LunchTime.query.all()
    assert len(lunches) == 2

    janes_lunch = lunches[-1]
    johns_lunch = lunches[0]

    assert isinstance(janes_lunch.timeOut, datetime)
    assert janes_lunch.timeOut == datetime(2020, 7, 15, 12, 30)
    assert janes_lunch.employee_id == 2

