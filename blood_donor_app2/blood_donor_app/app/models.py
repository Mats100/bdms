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
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    pulse_rate = db.Column(db.Integer, nullable=False)
    haemoglobin = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.Boolean, nullable=False)
    allergies = db.Column(db.Boolean, nullable=False)
    blood_test = db.Column(db.Boolean, nullable=False)
    cardiac_problems = db.Column(db.Boolean, nullable=False)
    bleeding_disorders = db.Column(db.Boolean, nullable=False)
    medication = db.Column(db.Boolean, nullable=False)

class BloodGroup(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
