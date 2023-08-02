import smtplib
from email.mime.text import MIMEText

import flask
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_required, logout_user, login_user, current_user
from app.forms import DonorDataForm, LoginForm, PasswordChangeForm, \
    DonorProfileUpdateForm, DonorSearchForm, RequestBlood
from app.database import db
from app.models import Donor, Campaign, BloodRequest
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('donor', __name__)


@bp.route('/dashboard')
@login_required
def donor_dashboard():
    if current_user.is_authenticated:
        return render_template('donor_dashboard/dashboard.html')
    else:
        flash('You need to log in to access the dashboard.')
        return render_template('donor_dashboard/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = DonorDataForm()

    if form.validate_on_submit():
        # email = form.email.data
        # donor_email = Donor.query.filter_by(email=form.email.data).first()
        # if form.email.data == donor_email.email:
        #     flash('email already exists.', 'danger')
        #     return render_template('donor_dashboard/register.html', form=form)
        #
        # donor_username = Donor.query.filter_by(username=form.username.data).first()
        #
        # if form.username.data == donor_username.username:
        #     flash('username already exists.', 'danger')
        #     return render_template('donor_dashboard/register.html', form=form)

        if form.age.data < 18 or form.age.data > 65:
            flash('Age must be between 18 and 65.')
            return render_template('donor_dashboard/register.html', form=form)
        if form.age.data < 0 or form.weight.data < 0 or form.pulse_rate.data < 0 or form.haemoglobin.data < 0 or form.blood_pressure.data < 0 or form.temperature.data < 0:
            flash('Please enter positive values for age, weight, pulse rate, haemoglobin, blood pressure, '
                  'and temperature.')
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
    if flask.request.method == "POST":
        session.pop('_flashes', None)
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
            login_user(donor)
            return redirect(url_for('donor.donor_dashboard'))
        else:
            flash('Invalid username or password.')
    if flask.request.method == "GET":
        session.pop('_flashes', None)

    return render_template('donor_dashboard/login.html', form=form)


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = DonorProfileUpdateForm()

    if 'donor_id' not in session:
        flash('Please log in to update your profile.', '/process_emailerror')
        return redirect(url_for('donor.login'))

    donor_id = session['donor_id']
    donor = Donor.query.get(donor_id)

    if form.validate_on_submit():
        donor.name = form.name.data
        donor.age = form.age.data
        donor.contact_number = form.contact_number.data
        donor.address = form.address.data

        db.session.commit()
        return redirect(url_for('donor.update_profile'))

    form.name.data = donor.name
    form.age.data = donor.age
    form.contact_number.data = donor.contact_number
    form.address.data = donor.address

    return render_template('donor_dashboard/user_profile.html', form=form)


@bp.route('/about', methods=['GET'])
@login_required
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


@bp.route('/contact', methods=['GET', 'POST'])
@login_required
def contact_us():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        msg = MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        msg["Subject"] = "Donor Feedback Submission"
        msg["From"] = "bdmsystm@gmail.com"
        msg["To"] = "railpower15@gmail.com"
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("bdmsystm@gmail.com", "uolksibdermwwqbf")
                server.sendmail("bdmsystm@gmail.com", "railpower15@gmail.com", msg.as_string())
                return "Thank you for your message!"
        except Exception as e:
            return f"Error: {e}"
    return render_template('donor_dashboard/contact-us.html')


@bp.route('/donor-list', methods=['GET'])
@login_required
def donor_list():
    donors = Donor.query.all()
    return render_template('donor_dashboard/donor-list.html', donors=donors)


@bp.route('/campaign_details', methods=['GET'])
@login_required
def get_campaign():
    campaigns = Campaign.query.all()
    return render_template('donor_dashboard/campaign_details.html', campaigns=campaigns)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_donor():
    search_form = DonorSearchForm()
    results = []
    if search_form.validate_on_submit():
        blood_type = search_form.blood_type.data
        if blood_type:
            results = Donor.query.filter_by(blood_type=blood_type).all()
    return render_template('donor_dashboard/donor_search.html', form=search_form, results=results)


@bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        username = form.username.data
        donor = Donor.query.filter_by(username=username).first()

        if check_password_hash(donor.password, form.current_password.data):
            hashed_password = generate_password_hash(form.new_password.data)
            donor.password = hashed_password
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('donor.login'))
        else:
            flash('Invalid current password!', 'error')

    return render_template('donor_dashboard/forget_password.html', form=form)


@bp.route('/request', methods=['GET', 'POST'])
@login_required
def blood_request():
    form = RequestBlood()
    donor_id = session['donor_id']
    donor = Donor.query.get(donor_id)
    if form.validate_on_submit():
        blood_req = BloodRequest(donor_id=donor.id, group=form.group.data)
        db.session.add(blood_req)
        db.session.commit()
        return render_template('donor_dashboard/dashboard.html', form=form)
    return render_template('donor_dashboard/request.html', form=form, donor=donor)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('donor_id', None)
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('donor.login'))
