"""
1. For testing, create a fake dataset and get the chart to output


"""
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from datetime import datetime

data = {
    "workers": ["zlopez", "jspence", "aying"],
    "timeOut": [datetime(2020, 8, 1, time) for time in [12, 13, 14]],
    "timeIn": [datetime(2020, 8, 1, time) for time in [13, 14, 15]],
}

source = ColumnDataSource(data)


def create_chart(source):
    """
    create a bar chart

    Parameters

    workers : a list of all workers. ([emp.username for emp in Employee.query.all()])
    """
    p = figure(
        plot_width=800,
        plot_height=800,
        title="Lunch Times",
        x_axis_type="datetime",
        y_range=workers,
    )

    p.hbar()

