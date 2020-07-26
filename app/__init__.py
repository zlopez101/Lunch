from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    current_user,
    LoginManager,
    UserMixin,
    login_required,
    login_user,
)
from twilio.rest import Client
from app.forms import EmployeeOut, EmployeeLogin
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


login_manager.login_view = "login"
login_manager.login_message_category = "info"


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), default="password")
    phone_number = db.Column(db.String(60))
    email = db.Column(db.String(60))

    def __repr__(self):
        return f"Employee({self.username})"


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = EmployeeOut()
    if form.validate_on_submit():
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=form.data.message, from_="+12184268664", to="+17134306973",
        )
        print(message)

    return render_template("home.html", form=form, legend="Lunch Time!")


@app.route("/login", methods=["GET", "POST"])
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
                url_for("home")
            )  # if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful", "danger")
    return render_template("login.html", form=form, legend="Please Login")


@app.route("/profile/<int:userid>", methods=["GET", "POST"])
@login_required
def profile(userid):
    pass
