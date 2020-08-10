import os
from datetime import datetime
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20_15
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models.tools import HoverTool
from twilio.rest import Client
from flask_mail import Message

from app.models import LunchTime, Employee


def create_mail_message(Lunch):
    """
    Should send an email to everyone 

    Parameters
    Lunch : a LunchTime 
    """
    recipients = [
        emp.email for emp in Employee.query.filter_by(preferred="email").all()
    ]
    msg = Message(
        f"{Employee.query.filter_by(id=Lunch.employee_id)} is taking a lunch from {Lunch.timeOut} to {Lunch.timeIn}. Please cover the their shift.",
        recipients=recipients,
    )
    return msg


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
    today = datetime.today()
    beg, end = [
        datetime(today.year, today.month, today.day),
        datetime(today.year, today.month, today.day, 23, 59),
    ]

    source = ColumnDataSource(data=dict(workers=[], timeIn=[], timeOut=[]))
    for worker in workers:
        todays_lunch = LunchTime.query.filter(
            LunchTime.employee_id == worker.id,
            LunchTime.timeIn > beg,
            LunchTime.timeOut < end,
        ).first()
        if todays_lunch:
            dct = {
                "workers": [worker.username],
                "timeIn": [todays_lunch.timeIn],
                "timeOut": [todays_lunch.timeOut],
            }
            source.stream(dct)
        else:
            pass

    return source


def _create_chart(source):
    """
    create a bar chart

    Parameters
    data : a dictionary
    # source : a ColumnDataSource created by `create_source` function
    """
    # hover tool configuration

    TOOLTIPS = [
        ("worker", "@workers"),
        ("time Out", "@timeOut{%r}"),
        ("time In", "@timeIn{%r}"),
    ]

    plot = figure(
        plot_width=800,
        plot_height=400,
        title="Lunch Times",
        x_axis_type="datetime",
        # x_range=[datetime(2020, 8, 3, 8), datetime(2020, 8, 3, 17)],
        y_range=source.data["workers"],
        toolbar_location=None,
        tools="",
    )

    plot.hbar(
        y="workers",
        height=0.5,
        left="timeOut",
        right="timeIn",
        color=factor_cmap("workers", Category20_15, source.data["workers"]),
        # legend_field="workers",
        source=source,
    )

    plot.add_tools(
        HoverTool(
            tooltips=TOOLTIPS,
            formatters={"@timeIn": "datetime", "@timeOut": "datetime"},
        )
    )
    plot.xaxis[0].formatter = DatetimeTickFormatter(hourmin="%H:%M")
    return plot


def create_chart(workers):
    data = create_source(workers)
    return _create_chart(data)
