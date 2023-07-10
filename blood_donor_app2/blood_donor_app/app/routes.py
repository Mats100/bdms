from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from blood_donor_app2.blood_donor_app.app.forms import DonorRegistrationForm, DonorSearchForm, DonorDeleteForm, \
    DonorUpdateForm, BloodGroupForm
from blood_donor_app2.blood_donor_app.app.models import Donor, BloodGroup
from blood_donor_app2.blood_donor_app.app import db

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return redirect(url_for('donor.login'))


@bp.route('/donor_register', methods=['GET', 'POST'])
@login_required
def donor_register():
    form = DonorRegistrationForm()
    LOW_BLOOD_GROUP_THRESHOLD = 5

    if form.validate_on_submit():
        donor = Donor(name=form.name.data, age=form.age.data, contact_number=form.contact_number.data,
                      blood_type=form.blood_type.data)
        db.session.add(donor)
        db.session.commit()
        flash('Donor registered successfully!', 'success')

        blood_group = BloodGroup.query.filter_by(group=form.blood_type.data).first()
        if blood_group and blood_group.quantity <= LOW_BLOOD_GROUP_THRESHOLD:
            flash(f'Alert: Low quantity of {blood_group.group} blood group!')

        return redirect(url_for('admin.dashboard', donor_id=donor.id))

    return render_template('donor/register.html', form=form, LOW_BLOOD_GROUP_THRESHOLD=LOW_BLOOD_GROUP_THRESHOLD)


@bp.route('/donor_search', methods=['GET', 'POST'])
@login_required
def donor_search():
    form = DonorSearchForm()
    if form.validate_on_submit():
        blood_type = form.blood_type.data

        if blood_type:
            donors = Donor.query.filter_by(blood_type=blood_type).all()
        else:
            donors = Donor.query.all()

        return render_template('donor/search.html', form=form, donors=donors)

    return render_template('donor/search.html', form=form)


@bp.route('/donor/<donor_id>')
@login_required
def donor_profile(donor_id):
    donor = Donor.query.get(donor_id)
    return render_template('donor/profile.html', donor=donor)


@bp.route('/donor_edit', methods=['GET', 'POST'])
@login_required
def edit_donor():
    donors = Donor.query.all()
    form = DonorUpdateForm()
    print(form.data)
    print(form.errors)

    if form.validate_on_submit():
        selected_donor_id = request.form.get('donor')

        if selected_donor_id:
            selected_donor = Donor.query.get(selected_donor_id)
            if selected_donor:
                selected_donor.name = form.name.data
                selected_donor.age = form.age.data
                selected_donor.contact_number = form.contact_number.data
                selected_donor.blood_type = form.blood_type.data

                try:
                    db.session.commit()
                    flash('Donor updated successfully.', 'success')
                    return redirect(url_for('main.donor_profile', donor_id=selected_donor.id))
                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    flash('Error updating donor.', 'error')
            else:
                flash('Donor not found.', 'error')
        else:
            flash('Invalid donor selection.', 'error')

    return render_template('donor/edit.html', form=form, donors=donors, selected_donor=None)


@bp.route('/donor/delete', methods=['GET', 'POST'])
@login_required
def delete_donor():
    form = DonorDeleteForm()
    form.name.choices = [(donor.id, donor.name) for donor in Donor.query.all()]
    if form.validate_on_submit():
        donor_id = form.name.data
        donor = Donor.query.get(donor_id)

        if donor:
            db.session.delete(donor)
            db.session.commit()
            return redirect(url_for('admin.dashboard'))

    return render_template('donor/delete.html', form=form)


@bp.route('/bloodgroup', methods=['GET', 'POST'])
@login_required
def blood_group():
    form = BloodGroupForm()

    if form.validate_on_submit():
        blood_group = BloodGroup.query.filter_by(group=form.group.data).first()

        if blood_group:
            blood_group.quantity += form.quantity.data
            db.session.commit()
        else:
            blood_group = BloodGroup(group=form.group.data, quantity=form.quantity.data)
            db.session.add(blood_group)
            db.session.commit()

        return redirect(url_for('main.blood_group'))

    blood_groups = BloodGroup.query.all()
    return render_template('donor/bloodgroup.html', form=form, blood_groups=blood_groups)


@bp.route('/bloodgroup/edit/<int:blood_group_id>', methods=['GET', 'POST'])
@login_required
def edit_blood_group(blood_group_id):
    blood_group = BloodGroup.query.get(blood_group_id)

    if not blood_group:
        flash('Blood group not found.')
        return redirect(url_for('main.blood_group'))

    form = BloodGroupForm(obj=blood_group)

    if form.validate_on_submit():
        blood_group.group = form.group.data
        blood_group.quantity = form.quantity.data
        db.session.commit()
        return redirect(url_for('main.blood_group'))

    return render_template('donor/edit_bloodgroup.html', form=form, blood_group_id=blood_group.id)


@bp.route('/bloodgroup/delete/<int:blood_group_id>', methods=['GET', 'POST'])
@login_required
def delete_blood_group(blood_group_id):
    blood_group = BloodGroup.query.get(blood_group_id)

    if not blood_group:
        flash('Blood group not found.')
        return redirect(url_for('main.blood_group'))

    db.session.delete(blood_group)
    db.session.commit()

    return redirect(url_for('main.blood_group'))
