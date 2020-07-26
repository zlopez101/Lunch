from flask_wtf import FlaskForm
from wtforms.fields import StringField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired


class EmployeeOut(FlaskForm):

    message = StringField("Pass on a message!")
    time_out = TimeField("Clocking out time")
    time_back_in = TimeField("Clocking in time")
    submit = SubmitField("Submit")


class EmployeeLogin(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ProfileForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone number", validators=[DataRequired()])
    preferred = SelectField(
        "Preferred Notification Style", coerce=int, choices=[(1, "phone"), (2, "email")]
    )
    submit = SubmitField("Submit")
