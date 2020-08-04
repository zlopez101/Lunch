from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TimeField,
    SubmitField,
    SelectField,
    PasswordField,
)
from wtforms.validators import DataRequired


class EmployeeOut(FlaskForm):

    message = StringField("Pass on a message!")
    time_out = TimeField("Clocking out time")
    time_back_in = TimeField("Clocking in time")
    submit = SubmitField("Submit")


class EmployeeLogin(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ProfileForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone number", validators=[DataRequired()])
    preferred = SelectField(
        "Preferred Notification Style",
        coerce=int,
        choices=[(1, "phone"), (2, "email")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")
