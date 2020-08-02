from app.users.utils import *
from app.models import Employee
from bokeh.models import ColumnDataSource
from datetime import datetime


def test_send_messages():
    """
    numbers = ["+17134306973"]

    send_messages("testing testing 123", numbers, testing=True)
    """
    pass


def test_create_source(app_tester, init_database):
    """
    GIVEN a user accessing the home page
    WHEN that user is signed in
    THEN the create source function should create a ColumnDataSource
    """
    data = create_source(Employee.query.all())
    cds = ColumnDataSource(data)
    assert isinstance(cds, ColumnDataSource)
    assert "workers" in cds.column_names

    assert isinstance(data["workers"], list)
    assert "JaneLong" in data["workers"]
    assert datetime(2020, 7, 15, 13, 30) in data["timeIn"]


def test_create_chart(app_tester, init_database):
    """
    GIVEN a set of preferencs by user
    WHEN a verified user accesses the home page
    THEN a chart must be created for displaying current information regarding who's out when.
    """
    source = create_source(Employee.query.all())
    html = create_chart(source)
