from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.forms import LoginForm, PasswordChangeForm
from blood_donor_app2.blood_donor_app.app.forms import DonorDataForm
from app import db
from app.models import Donor
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('donor', __name__)



@bp.route('/dashboard')
def donor_dashboard():
    return render_template('donor_dashboard/dashboard.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = DonorDataForm()
    # print(form)
    # print(form.data)
    # print(form.validate())
    # print(form.errors)
    if form.validate_on_submit():
        if form.age.data < 18 or form.age.data > 65:
            flash('Age must be between 18 and 65.')
            return render_template('donor_dashboard/register.html', form=form)
        donor = Donor(
            name=form.name.data,
            age=form.age.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            gender=form.gender.data,
            address=form.address.data,
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            weight=form.weight.data,
            blood_type=form.blood_type.data,
            pulse_rate=form.pulse_rate.data,
            haemoglobin=form.haemoglobin.data,
            blood_pressure=form.blood_pressure.data,
            temperature=form.temperature.data,
            disease=form.disease.data,
            allergies=form.allergies.data,
            blood_test=form.blood_test.data,
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
            flash('Invalid username or password.')

    return render_template('donor_dashboard/login.html', form=form)


@bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        donor_id = session['donor_id']
        donor = Donor.query.get(donor_id)

        if donor.password == form.current_password.data:
            donor.password = form.new_password.data
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('donor.login'))
        else:
            flash('Invalid current password!', 'error')

    return render_template('donor_dashboard/forget_password.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('donor_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('donor.login'))
