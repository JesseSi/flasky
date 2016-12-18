# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, abort, request
from flask.ext.login import login_required, \
    current_user, current_app
from wtforms_components import read_only as rr

from . import apply_blueprint
from .forms import ApplyForm, EditApplyForm, EditApplyAdminForm
from .. import db
from ..models import Apply


@apply_blueprint.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        apply = Apply(real_name=form.real_name.data,
                      mobile=form.mobile.data,
                      gender=form.gender.data,
                      home_address=form.home_address.data,
                      middle_school=form.middle_school.data,
                      id_card=form.id_card.data,
                      point=form.point.data,
                      ticket_number=form.ticket_number.data,
                      apply_profession=form.apply_profession.data,
                      apply_profession_category=form.apply_profession_category.data,
                      status=u'新申请',
                      author_id=current_user.id)
        db.session.add(apply)
        db.session.commit()
        flash('恭喜你,报名成功!')
        return redirect(url_for('main.index'))
    return render_template('apply/apply.html', form=form)


@apply_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    apply = Apply.query.get_or_404(id)
    if current_user.id != apply.author_id and \
            not current_user.is_administrator():
        abort(403)
    form = EditApplyForm()
    if form.close.data:
        return redirect(url_for('apply.show_applys'))
    if form.validate_on_submit():
        apply.id = id
        apply.real_name = form.real_name.data
        apply.gender = form.gender.data
        apply.home_address = form.home_address.data
        apply.middle_school = form.middle_school.data
        apply.mobile = form.mobile.data
        apply.id_card = form.id_card.data
        apply.point = form.point.data
        apply.ticket_number = form.ticket_number.data
        apply.apply_profession = form.apply_profession.data
        apply.apply_time = form.apply_time.data
        db.session.add(apply)
        flash('报名信息修改成功.')
        return redirect(url_for('apply.show_applys'))
    form.apply_id.data = apply.id
    form.real_name.data = apply.real_name
    form.gender.data = apply.gender
    form.home_address.data = apply.home_address
    form.middle_school.data = apply.middle_school
    form.mobile.data = apply.mobile
    form.id_card.data = apply.id_card
    form.point.data = apply.point
    form.ticket_number.data = apply.ticket_number
    form.apply_profession.data = apply.apply_profession
    form.apply_profession_category.data = apply.apply_profession_category
    form.apply_time.data = apply.apply_time
    form.status.data = apply.status
    if form.status.data == u'已处理':
        rr(form.submit)
    rr(form.status)
    return render_template('apply/edit_apply.html', form=form)


@apply_blueprint.route('/edit_admin/<id>', methods=['GET', 'POST'])
@login_required
def edit_admin(id):
    apply = Apply.query.get_or_404(id)
    if not current_user.is_administrator():
        abort(403)
    form = EditApplyAdminForm()
    if form.close.data:
        return redirect(url_for('apply.show_applys'))
    if form.validate_on_submit():
        apply.id = id
        apply.real_name = form.real_name.data
        apply.gender = form.gender.data
        apply.home_address = form.home_address.data
        apply.middle_school = form.middle_school.data
        apply.mobile = form.mobile.data
        apply.id_card = form.id_card.data
        apply.point = form.point.data
        apply.ticket_number = form.ticket_number.data
        apply.apply_profession = form.apply_profession.data
        apply.apply_profession_category = form.apply_profession_category.data
        apply.apply_time = form.apply_time.data
        apply.status = form.status.data
        db.session.add(apply)
        flash('报名信息修改成功.')
        return redirect(url_for('apply.show_applys'))
    form.apply_id.data = apply.id
    form.real_name.data = apply.real_name
    form.gender.data = apply.gender
    form.home_address.data = apply.home_address
    form.middle_school.data = apply.middle_school
    form.mobile.data = apply.mobile
    form.id_card.data = apply.id_card
    form.point.data = apply.point
    form.ticket_number.data = apply.ticket_number
    form.apply_profession.data = apply.apply_profession
    form.apply_profession_category.data = apply.apply_profession_category
    form.apply_time.data = apply.apply_time
    form.status.data = apply.status
    return render_template('apply/edit_apply.html', form=form)


@apply_blueprint.route('/show_applys')
@login_required
def show_applys():
    page = request.args.get('page', 1, type=int)
    if current_user.is_administrator():
        query = Apply.query
    else:
        query = Apply.query.filter_by(author_id=current_user.id)
    pagination = query.order_by(Apply.apply_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    applys = pagination.items
    return render_template('apply/show_applys.html', applys=applys, pagination=pagination)
