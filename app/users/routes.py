from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from bokeh.resources import CDN
from bokeh.embed import components
from app import bcrypt, db, mail
from app.models import Employee, LunchTime
from app.users.forms import EmployeeLogin, EmployeeOut, ProfileForm
from app.users.utils import send_messages, create_chart, create_mail_message
from datetime import date, datetime
import threading

users = Blueprint("users", __name__)


@users.route("/", methods=["GET", "POST"])
@login_required
def lunchbuddy():
    # chart
    plot = create_chart(Employee.query.all())
    script, div = components(plot)

    # form
    form = EmployeeOut()
    if form.validate_on_submit():
        timeOut = datetime.combine(date.today(), form.time_out.data)
        timeIn = datetime.combine(date.today(), form.time_back_in.data)
        new_lunch = LunchTime(
            timeOut=timeOut, timeIn=timeIn, employee_id=current_user.id,
        )

        db.session.add(new_lunch)
        db.session.commit()

        # send emails
        mail.send(create_mail_message(new_lunch))
        # send texts

        flash("Your message has been saved!", "success")
        return redirect(url_for("users.lunchbuddy"))

    return render_template(
        "lunchbuddy.html",
        form=form,
        legend="Lunch Time!",
        resources=CDN.render(),
        the_script=script,
        the_div=div,
    )


@users.route("/plot")
def plot():
    plot = create_chart(Employee.query.all())
    script, div = components(plot)
    return render_template(
        "plot.html", resources=CDN.render(), the_script=script, the_div=div,
    )


@users.route("/login", methods=["GET", "POST"])
def login():
    form = EmployeeLogin()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(username=form.username.data).first()
        if employee and bcrypt.check_password_hash(
            employee.password, form.password.data
        ):
            login_user(employee)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("users.lunchbuddy"))
            )

        else:
            flash("Login Unsuccessful", "danger")
    return render_template("login.html", form=form, legend="Please Login")


@users.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    emp = Employee.query.filter_by(id=current_user.id).first()
    form = ProfileForm()
    if form.validate_on_submit():
        emp.email = form.email.data
        emp.phone_number = form.phone.data
        emp.preferred = form.preferred.data
        db.session.commit()
        return redirect(url_for("users.lunchbuddy"))
    elif request.method == "GET":
        form.email.data = emp.email
        form.phone.data = emp.phone_number

    return render_template(
        "profile.html",
        title="Profile",
        Legend=f"{emp.username}'s preferences",
        form=form,
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/reset")
def reset_password():
    pass


@users.route("/display")
def display():
    """
    will display everyone's lunch times as a bar graph
    """
    pass
