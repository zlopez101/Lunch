from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), default="password")
    phone_number = db.Column(db.String(60))
    email = db.Column(db.String(60))
    preferred = db.Column(db.String(60))

    def __repr__(self):
        return f"Employee({self.username})"


# class LunchTime(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timeIn = db.T