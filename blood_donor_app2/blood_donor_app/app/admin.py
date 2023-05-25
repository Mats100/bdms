from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms import LoginForm, ProfileUpdateForm, PasswordChangeForm, RegisterForm
from app.models import Admin
from app import db
from app.models import Donor,BloodGroup

bp = Blueprint('admin', __name__)


@bp.route('/')
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

    return render_template('admin/dashboard.html', blood_group_percentages=blood_group_percentages, donor_count=donor_count)




@bp.route('/donors')
def donor_list():
    donors = Donor.query.all()

    return render_template('admin/donor_list.html', donors=donors)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        admin = Admin(
            name=form.name.data,
            age=form.age.data,
            contact_number=form.contact_number.data,
            address=form.address.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('admin.login'))

    return render_template('admin/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.password == password:
            session['admin_id'] = admin.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('admin/login.html', form=form)


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        admin_id = session['admin_id']
        admin = Admin.query.get(admin_id)

        admin.name = form.name.data
        admin.contact_number = form.contact_number.data
        admin.address = form.address.data

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    return render_template('admin/profile.html', form=form)


@bp.route('/password_change', methods=['GET', 'POST'])
def password_change():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        admin_id = session['admin_id']
        admin = Admin.query.get(admin_id)

        if admin.password == form.current_password.data:
            admin.password = form.new_password.data
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('admin.login'))
        else:
            flash('Invalid current password!', 'error')

    return render_template('admin/password_change.html', form=form)


@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin.login'))
