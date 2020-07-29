from app import db, bcrypt, create_app
from app.models import Employee
from app.config import Configuration

app = create_app(Configuration)
with app.app_context():
    db.create_all()
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

    for name in lst:
        emp = Employee(
            username=name, password=bcrypt.generate_password_hash("password")
        )
        db.session.add(emp)
        db.session.commit()
