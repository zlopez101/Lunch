from app import db, Employee, bcrypt

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
    emp = Employee(username=name, password=bcrypt.generate_password_hash("password"))
    db.session.add(emp)
    db.session.commit()
