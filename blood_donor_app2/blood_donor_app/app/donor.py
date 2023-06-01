from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms import DonorDataForm, LoginForm
from app import db
from app.models import Donor
from werkzeug.security import check_password_hash

bp = Blueprint('donor', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = DonorDataForm()

    if form.validate_on_submit():
        if form.age.data < 18 or form.age.data > 65:
            flash('Age must be between 18 and 65.', 'error')
            return render_template('donor_dashboard/register.html', form=form)

        donor = Donor(
            donor_id=form.donor_id.data,
            name=form.name.data,
            age=form.age.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            gender=form.gender.data,
            address=form.address.data,
            body_weight=form.body_weight.data,
            blood_type=form.blood_type.data,
            pulse_rate=form.pulse_rate.data,
            haemoglobin=form.haemoglobin.data,
            blood_pressure=form.blood_pressure.data,
            temperature=form.temperature.data,
            disease=form.disease.data,
            allergies=form.allergies.data,
            positive_test=form.positive_test.data,
            cardiac_problems=form.cardiac_problems.data,
            bleeding_disorders=form.bleeding_disorders.data,
            medication=form.medication.data
        )
        db.session.add(donor)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('donor.login'))

    return render_template('donor_dashboard/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        donor = Donor.query.filter_by(username=username).first()

        if donor and check_password_hash(donor.password, password):
            session['donor_id'] = donor.id
            return redirect(url_for('donor.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('donor_dashboard/login.html', form=form)
