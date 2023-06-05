from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, NumberRange

from app.models import Donor, Admin


class RegisterForm(FlaskForm):
    name = StringField('Fullname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProfileUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Password')


class DonorRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    blood_type = SelectField('Blood Type',
                             choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                      ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], validators=[DataRequired()])
    submit = SubmitField('Register')


class DonorSearchForm(FlaskForm):
    name = StringField('Name')
    blood_type = SelectField('Blood Type',
                             choices=[('', 'Any'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                      ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    submit = SubmitField('Search')


class DonorUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    blood_type = SelectField('Blood Type',
                             choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                      ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], validators=[DataRequired()])
    submit = SubmitField('Update')


class DonorDeleteForm(FlaskForm):
    name = SelectField('Name', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super(DonorDeleteForm, self).__init__(*args, **kwargs)
        self.name.choices = [(donor.id, donor.name) for donor in Donor.query.all()]


class BloodGroupForm(FlaskForm):
    group = StringField('Blood Group', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Save')


class DonorDataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=65)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=8, max=8)])
    email = StringField('Email Address', validators=[Email()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    blood_type = SelectField('Blood Group',
                             choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                      ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')],
                             validators=[DataRequired()])
    pulse_rate = IntegerField('Pulse Rate', validators=[DataRequired()])
    haemoglobin = IntegerField('Haemoglobin', validators=[DataRequired()])
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired()])
    temperature = StringField('Temperature', validators=[DataRequired()])
    disease = BooleanField('Do you suffer from any disease?')
    allergies = BooleanField('Do you have any allergies?')
    blood_test = BooleanField('Have you ever had a positive blood test for HbsAg, Hcv, HIV?')
    cardiac_problems = BooleanField('Do you have any cardiac problems?')
    bleeding_disorders = BooleanField('Do you suffer from any bleeding disorders?')
    medication = BooleanField('Do you take any medication?')
    submit = SubmitField('Register')


class DonorProfileUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=65)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=8, max=8)])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')
