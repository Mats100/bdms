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
    address = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(10), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    blood_type = db.Column(db.String(10), nullable=False)
    pulse_rate = db.Column(db.Integer, nullable=True)
    haemoglobin = db.Column(db.Float, nullable=True)
    blood_pressure = db.Column(db.String(20), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    disease = db.Column(db.String(50), nullable=True)
    allergies = db.Column(db.String(50), nullable=True)
    blood_test = db.Column(db.String(10), nullable=True)
    cardiac_problems = db.Column(db.String(10), nullable=True)
    bleeding_disorders = db.Column(db.String(10), nullable=True)
    medication = db.Column(db.String(50), nullable=True)



class BloodGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
