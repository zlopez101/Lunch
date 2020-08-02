from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Configuration


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
    }


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.users.routes import users

    app.register_blueprint(users)

    return app
