import os
from bokeh.plotting import figure, output_file, show

from twilio.rest import Client


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


def create_chart():
    """
    create a bar chart
    """
    p = figure(
        plot_width=800,
        plot_height=800,
        title="Lunch Times",
        x_axis_type="datetime",
        y_axis_label="Worker",
    )
