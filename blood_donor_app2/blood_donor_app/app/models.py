from app import db


class Admin(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Donor(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    # Add other donor fields as needed

class BloodGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
