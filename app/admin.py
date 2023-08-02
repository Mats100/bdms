import flask
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_required, logout_user, login_user
from app.forms import RegisterForm, ProfileUpdateForm, PasswordChangeForm, LoginForm
from app import db
from app.mail import send_email
from app.models import Donor, BloodGroup, BloodRequest
from app.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('admin', __name__)


@bp.route('/dashboard')
@login_required
def dashboard():
    donor_count = Donor.query.count()
    blood_groups = BloodGroup.query.all()
    total_count = sum(blood_group.quantity for blood_group in blood_groups)

    blood_group_percentages = [
        {
            'group': blood_group.group,
            'percentage': (blood_group.quantity / total_count) * 100 if total_count != 0 else 0
        }
        for blood_group in blood_groups
    ]
    return render_template('admin/dashboard.html', blood_group_percentages=blood_group_percentages,
                           donor_count=donor_count)


@bp.route('/donors')
def donor_list():
    donors = Donor.query.all()
    return render_template('admin/donor_list.html', donors=donors)


@bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.age.data < 0:
            flash('Age cannot be negative.')
            return render_template('admin/register.html', form=form)
        admin = Admin(
            name=form.name.data,
            age=form.age.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            address=form.address.data,
            username=form.username.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(admin)
        send_email("Subject", "registered", "railpower15@gmail.com")
        db.session.commit()
        return redirect(url_for('admin.login'))
    if request.method == "POST":
        session.pop('_flashes', None)

    return render_template('admin/register.html', form=form)


@bp.route('/request', methods=['GET', 'POST'])
@login_required
def blood_request():
    requests_blood = BloodRequest.query.filter_by(status=False).all()
    return render_template('admin/requests_blood.html', requests_blood=requests_blood)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    if flask.request.method == "GET":
        session.pop('_flashes', None)
    return render_template('admin/login.html', form=form)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        admin_id = session['admin_id']
        admin = Admin.query.get(admin_id)

        admin.name = form.name.data
        admin.age = form.age.data
        admin.contact_number = form.contact_number.data
        admin.address = form.address.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))

    admin_id = session['admin_id']
    admin = Admin.query.get(admin_id)
    form.name.data = admin.name
    form.age.data = admin.age
    form.contact_number.data = admin.contact_number
    form.address.data = admin.address

    return render_template('admin/profile.html', form=form)


@bp.route('/password_change', methods=['GET', 'POST'])
def password_change():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        username = form.username.data
        admin = Admin.query.filter_by(username=username).first()

        if check_password_hash(admin.password, form.current_password.data):
            hashed_password = generate_password_hash(form.new_password.data)
            admin.password = hashed_password
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('admin.login'))
        else:
            flash('Invalid current password!', 'error')

    return render_template('admin/password_change.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('admin_id', None)
    session.clear()
    return redirect(url_for('admin.login'))
