from datetime import datetime

from flask_login import UserMixin

from app.database import db


class Admin(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Donor(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    occupation = db.Column(db.String, nullable=True)
    blood_type = db.Column(db.String(10), nullable=False)
    pulse_rate = db.Column(db.Integer, nullable=True)
    haemoglobin = db.Column(db.Float, nullable=True)
    blood_pressure = db.Column(db.Integer, nullable=True)
    temperature = db.Column(db.Integer, nullable=True)
    disease = db.Column(db.Boolean, nullable=True)
    allergies = db.Column(db.Boolean, nullable=True)
    blood_test = db.Column(db.Boolean, nullable=True)
    cardiac_problems = db.Column(db.Boolean, nullable=True)
    bleeding_disorders = db.Column(db.Boolean, nullable=True)
    medication = db.Column(db.Boolean, nullable=True)

    requests = db.relationship('BloodRequest', backref='donor')


class BloodDonation(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'))
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class BloodRequest(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'))
    group = db.Column(db.String(10), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=True, default=False)


class BloodGroup(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)


class Campaign(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

