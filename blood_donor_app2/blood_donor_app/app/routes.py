from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import DonorRegistrationForm, DonorSearchForm, DonorDeleteForm, DonorUpdateForm, BloodGroupForm
from app.models import Donor, BloodGroup
from app import db

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return redirect(url_for('admin.login'))


@bp.route('/donor_register', methods=['GET', 'POST'])
def donor_register():
    form = DonorRegistrationForm()
    LOW_BLOOD_GROUP_THRESHOLD = 5

    if form.validate_on_submit():
        donor = Donor(name=form.name.data, blood_type=form.blood_type.data)
        db.session.add(donor)
        db.session.commit()
        flash('Donor registered successfully!', 'success')

        # Check blood group level
        blood_group = BloodGroup.query.filter_by(group=form.blood_type.data).first()
        if blood_group and blood_group.quantity <= LOW_BLOOD_GROUP_THRESHOLD:
            flash(f'Alert: Low quantity of {blood_group.group} blood group!')

        return redirect(url_for('main.donor_profile', donor_id=donor.id))

    return render_template('donor/register.html', form=form, LOW_BLOOD_GROUP_THRESHOLD=LOW_BLOOD_GROUP_THRESHOLD)


@bp.route('/donor/search', methods=['GET', 'POST'])
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
def donor_profile(donor_id):
    donor = Donor.query.get(donor_id)
    return render_template('donor/profile.html', donor=donor)


@bp.route('/donor/edit', methods=['GET', 'POST'])
def edit_donor():
    form = DonorUpdateForm()

    if form.validate_on_submit():
        donor = Donor.query.filter_by(name=form.name.data).first()
        if donor:
            donor.name = form.name.data
            donor.blood_type = form.blood_type.data
            db.session.commit()
            flash('Donor updated successfully.', 'success')
            return redirect(url_for('main.donor_profile', donor_id=donor.id))
        else:
            flash('Donor not found.', 'error')

    return render_template('donor/edit.html', form=form)


@bp.route('/donor/delete', methods=['GET', 'POST'])
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
def blood_group():
    form = BloodGroupForm()

    if form.validate_on_submit():
        blood_group = BloodGroup.query.filter_by(group=form.group.data).first()

        if blood_group:
            flash('Blood group already exists.')
        else:
            blood_group = BloodGroup(group=form.group.data, quantity=form.quantity.data)
            db.session.add(blood_group)
            db.session.commit()
            flash('Blood group added successfully!')

        return redirect(url_for('main.blood_group'))

    blood_groups = BloodGroup.query.all()
    return render_template('donor/bloodgroup.html', form=form, blood_groups=blood_groups)


@bp.route('/bloodgroup/edit/<int:blood_group_id>', methods=['GET', 'POST'])
def edit_blood_group(blood_group_id):
    blood_group = BloodGroup.query.get(blood_group_id)

    if not blood_group:
        flash('Blood group not found.')
        return redirect(url_for('main.blood_group'))

    form = BloodGroupForm(obj=blood_group)

    if form.validate_on_submit():
        blood_group.group = form.group.data
        db.session.commit()
        flash('Blood group updated successfully!', 'success')
        return redirect(url_for('main.blood_group'))

    return render_template('donor/edit_bloodgroup.html', form=form)


@bp.route('/bloodgroup/delete/<int:blood_group_id>', methods=['GET', 'POST'])
def delete_blood_group(blood_group_id):
    blood_group = BloodGroup.query.get(blood_group_id)

    if not blood_group:
        flash('Blood group not found.', 'danger')
        return redirect(url_for('main.blood_group'))

    db.session.delete(blood_group)
    db.session.commit()
    flash('Blood group deleted successfully!', 'success')

    return redirect(url_for('main.blood_group'))
