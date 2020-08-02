import os
from datetime import datetime
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource
from twilio.rest import Client

from app.models import LunchTime


def send_messages(message, numbers, testing=False):
    """
    for the appropriate numbers, send text messages with update on lunch times
    """
    if testing:
        account_sid = os.environ.get("TWILIO_TEST_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_TEST_AUTH_TOKEN")
        from_ = "+15005550006"
    else:
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_ = "+12184268664"
    client = Client(account_sid, auth_token)
    for number in numbers:
        message = client.messages.create(body=message, from_=from_, to=number)


def create_source(workers):
    """
    create the column data source for the chart
    Should accept the list of workers, then retrieve the times for each worker and zip into ColumnDataSource
    
    Parameters
    workers : a BaseQuery object of Employees ([emp.username for emp in Employee.query.all()])
    """
    # today = datetime.today()
    # # right now there is no function to auto delete a LunchTime, so need to filter results
    # _range = [
    #     datetime(today.year, today.month, today.day, x) for x in [8, 18]
    # ]  # creates a bottom and top filter.
    dct = {
        "workers": [],
        "timeIn": [],
        "timeOut": [],
    }
    for worker in workers:
        dct["workers"].append(worker.username)
        lunchtime = LunchTime.query.filter_by(employee_id=worker.id).all()[0]
        dct["timeIn"].append(lunchtime.timeIn)
        dct["timeOut"].append(lunchtime.timeOut)

    return dct


def create_chart(data):
    """
    create a bar chart

    Parameters
    data : a dictionary
    # source : a ColumnDataSource created by `create_source` function
    """
    source = ColumnDataSource(data)
    p = figure(
        plot_width=800,
        plot_height=400,
        title="Lunch Times",
        x_axis_type="datetime",
        x_range=[datetime(2020, 8, 1, 8), datetime(2020, 8, 1, 17)],
        y_range=data["workers"],
        toolbar_location=None,
        tools="",
    )

    p.hbar(
        y="workers",
        height=0.5,
        left="timeOut",
        right="timeIn",
        color="color",
        # legend_field="workers",
        source=source,
    )

    return file_html(p, CDN, "Lunch Times scheduled")

