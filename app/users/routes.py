from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
from bokeh.resources import CDN
from bokeh.embed import components
from app import bcrypt, db
from app.models import Employee, LunchTime
from app.users.forms import EmployeeLogin, EmployeeOut, ProfileForm
from app.users.utils import send_messages, create_chart
from datetime import date, datetime

users = Blueprint("users", __name__)


@users.route("/", methods=["GET", "POST"])
@login_required
def lunchbuddy():
    plot = create_chart(Employee.query.all())
    script, div = components(plot)
    form = EmployeeOut()
    # employees = Employee.query.filter(
    #     Employee.username != Employee.query.filter_by(id=userid).first().username
    # ).all()
    numbers = [employee.phone_number for employee in Employee.query.all()]
    if form.validate_on_submit():
        timeOut = datetime.combine(date.today(), form.time_out.data)
        timeIn = datetime.combine(date.today(), form.time_back_in.data)
        new_lunch = LunchTime(
            timeOut=timeOut, timeIn=timeIn, employee_id=current_user.id,
        )
        db.session.add(new_lunch)
        db.session.commit()
        # send_messages(form.message.data, numbers)
        flash("Your message has been saved!", "Sucesss")

    return render_template(
        "lunchbuddy.html",
        form=form,
        legend="Lunch Time!",
        resources=CDN.render(),
        the_script=script,
        the_div=div,
    )


# @users.route("/add_lunch<int:userid>", methods=['GET', "POST"])
# @login_required
# def add_lunch():
#     _me =  Employee.query.filter_by(id=current_user).first()
#     form = EmployeeOut()
#     if form.validate_on_submit():

#         flash("Your message has been saved!", "Sucesss")
#     return render_template("add_lunch.html", form=form, legend='Lunch Time!')


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
