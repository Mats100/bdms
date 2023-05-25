from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length

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