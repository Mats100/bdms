from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from blood_donor_app2.blood_donor_app.app.forms import DonorDataForm, LoginForm, PasswordChangeForm, \
    DonorProfileUpdateForm, DonorSearchForm
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
    # print(form.errors)
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        donor = Donor.query.filter_by(username=username).first()
        # print(donor.password)
        # print(check_password_hash(donor.password, password))
        if donor and check_password_hash(donor.password, password):
            session['donor_id'] = donor.id
            return redirect(url_for('donor.donor_dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('donor_dashboard/login.html', form=form)


@bp.route('/update', methods=['GET', 'POST'])
def update_profile():
    form = DonorProfileUpdateForm()

    if request.method == "POST":
        donor_id = session['donor_id']
        donor = Donor.query.get(donor_id)

        donor.name = form.name.data
        donor.age = form.age.data
        donor.contact_number = form.contact_number.data
        donor.address = form.address.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('donor.update_profile'))
    return render_template('donor_dashboard/user_profile.html', form=form)


@bp.route('/about', methods=['GET'])
def about():
    rules = [
        "Donors must be at least 18 years old or at most 65 years old.",
        "If a donor has the desire to 'give back', he/she can donate blood to the community every 3 months.",
        "No donation is allowed if the donor has any disease or is not in proper health condition.",
        "The blood in the blood stock expires after 35 days.",
        "Pregnant individuals are not eligible to donate; they should wait 6 weeks after giving birth.",
        "Donors should not give blood if they have AIDS or have ever had a positive HIV test.",
        "If a donor has had hepatitis, they are not eligible to donate blood.",
        "If the weight of the donor is between 45-50 kg, they can donate blood up to 350ml, and if it is greater than "
        "50kg, they can give 450ml at a time."
    ]

    return render_template('donor_dashboard/about.html', rules=rules)


@bp.route('/search', methods=['GET', 'POST'])
def search_donor():
    search_form = DonorSearchForm()
    results = []
    if search_form.validate_on_submit():
        name = search_form.name.data
        blood_type = search_form.blood_type.data
        if name and blood_type:
            results = Donor.query.filter_by(name=name, blood_type=blood_type).all()
        elif name:
            results = Donor.query.filter_by(name=name).all()
        elif blood_type:
            results = Donor.query.filter_by(blood_type=blood_type).all()
    return render_template('donor_dashboard/donor_search.html', form=search_form, results=results)

@bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        donor_id = session['donor_id']
        donor = Donor.query.get(donor_id)

        if check_password_hash(donor.password, form.current_password.data):
            hashed_password = generate_password_hash(form.new_password.data)
            donor.password = hashed_password
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('donor.login'))
        else:
            flash('Invalid current password!', 'error')

    return render_template('donor_dashboard/forget_password.html', form=form)
@bp.route('/donation_form', methods=['GET', 'POST'])



@bp.route('/logout')
def logout():
    session.pop('donor_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('donor.login'))
