from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from bokeh.resources import CDN

from app import bcrypt
from app.models import Employee
from app.users.forms import EmployeeLogin, EmployeeOut, ProfileForm
from app.users.utils import send_messages, create_chart

users = Blueprint("users", __name__)


@users.route("/<int:userid>", methods=["GET", "POST"])
@login_required
def lunchbuddy(userid):
    chart = create_chart()
    form = EmployeeOut()
    employees = Employee.query.filter(
        Employee.username != Employee.query.filter_by(id=userid).first().username
    ).all()
    numbers = [employee.phone_number for employee in employees]
    if form.validate_on_submit():
        send_messages(form.message.data, numbers)
        flash("Your message has been saved!", "Sucesss")

    return render_template(
        "lunchbuddy.html", form=form, legend="Lunch Time!", resources=CDN.render()
    )


@users.route("/", methods=["GET", "POST"])
@users.route("/login", methods=["GET", "POST"])
def login():
    form = EmployeeLogin()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(username=form.username.data).first()
        if employee and bcrypt.check_password_hash(
            employee.password, form.password.data
        ):
            login_user(employee)
            # next_page = request.args.get("next")
            return redirect(
                url_for("users.lunchbuddy", userid=int(employee.id))
            )  # if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful", "danger")
    return render_template("login.html", form=form, legend="Please Login")


@users.route("/profile/<int:userid>", methods=["GET", "POST"])
@login_required
def profile(userid):
    emp = Employee.query.filter_by(id=userid).first()
    form = ProfileForm()
    form.email.data = emp.email
    form.phone.data = emp.phone_number
    # form.preferred.data = emp.preferred
    if form.validate_on_submit():
        emp.email = form.email.data
        emp.phone_number = form.phone.data
        db.session.commit()
        return redirect(url_for("users.lunchbuddy"))
    return render_template(
        "profile.html",
        title="Profile",
        Legend=f"{emp.username}'s preferences",
        form=form,
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect("users.login")


@users.route("/reset")
def reset_password():
    pass


@users.route("/display")
def display():
    """
    will display everyone's lunch times as a bar graph
    """
    pass
