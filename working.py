"""
1. For testing, create a fake dataset and get the chart to output


"""
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import file_html
from bokeh.palettes import Category20_15
from datetime import datetime

lst = [
    "zlopez",
    "jcurtain",
    "dweinert",
    "carizpe",
    "marmstrong",
    "tmason",
    "idorantes",
    "kaguilar",
    "vwilliams",
    "mwilliams",
    "mkeener",
    "cvassar",
    "dthomas",
    "mflores",
    "mvillatoro",
]
timeOut = [11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14]
data = {
    "workers": lst,
    "timeOut": [datetime(2020, 8, 1, time) for time in timeOut],
    "timeIn": [datetime(2020, 8, 1, time) for time in [(x + 1) for x in timeOut]],
    "color": Category20_15,
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
        plot_height=400,
        title="Lunch Times",
        x_axis_type="datetime",
        x_range=[datetime(2020, 8, 1, 8), datetime(2020, 8, 1, 17)],
        y_range=lst,
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

    return p


create_chart(source)

