import pytest
from app.models import Employee, LunchTime
from datetime import datetime


def test_Employee(app_tester, init_database):
    """
    GIVEN new employee
    WHEN employee is added
    THEN check employees can be added and deleted from database
    """

    emp2 = Employee(username="testing", password="password", preferred="phone")
    init_database.session.add(emp2)
    init_database.session.commit()

    emps = Employee.query.all()
    assert len(emps) == 3
    assert emps[-1].username == "testing"

    phones = Employee.query.filter_by(preferred="phone").all()
    assert len(phones) == 2
    assert emps[0].username == "JohnDoe"

    init_database.session.delete(emp2)
    init_database.session.commit()

    emps = Employee.query.all()
    assert len(emps) == 2
    assert emps[-1].username == "JaneLong"
    assert emps[-1].phone_number == "jane's phone"


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


def test_get_todays_LunchTime(app_tester, init_database):
    """
    GIVEN multiple LunchTime entities for a worker
    WHEN a user accesses the website
    THEN only a LunchTime that is valid for today should be returned
    """
    today = datetime.today()
    beg, end = [
        datetime(today.year, today.month, today.day),
        datetime(today.year, today.month, today.day, 23, 59),
    ]

    # jane puts in a new lunch for today from 12:30 pm to 1:30 pm
    newlunch = LunchTime(
        timeIn=datetime(today.year, today.month, today.day, 12),
        timeOut=datetime(today.year, today.month, today.day, 13),
        employee_id=2,
    )
    init_database.session.add(newlunch)
    init_database.session.commit()

    janes_lunchs = LunchTime.query.filter_by(employee_id=2).all()
    assert len(janes_lunchs) == 2

    todays_lunch = LunchTime.query.filter(
        LunchTime.employee_id == 2, LunchTime.timeIn > beg, LunchTime.timeOut < end,
    ).first()

    assert todays_lunch.timeIn == newlunch.timeIn
    assert todays_lunch.timeOut == newlunch.timeOut
