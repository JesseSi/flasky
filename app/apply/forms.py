# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, DateTimeField, SelectField, SubmitField, HiddenField
from wtforms.validators import Required, Length
from wtforms import ValidationError
from ..models import Apply


class ReadOnlyWidgetProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('readonly', True)
        return self.widget(field, **kwargs)


def do_nothing(*args, **kwargs):
    pass


def read_only(field):
    field.widget = ReadOnlyWidgetProxy(field.widget)
    field.process = do_nothing
    field.populate_obj = do_nothing
    return field


class ApplyForm(Form):
    id = HiddenField(u'报名编号', )
    real_name = StringField(u'真实姓名', validators=[Required(u'必填项'), Length(1, 64)])
    mobile = StringField(u'手机号码', validators=[Required(u'必填项'), Length(11, 11, u'请填写正确的手机号码')])
    id_card = StringField(u'身份证号', validators=[Required(u'必填项'), Length(18, 18, u'请填写正确的身份证号')])
    point = IntegerField(u'高考分数', validators=[Required(u'必填项')])
    ticket_number = StringField(u'准考证号', validators=[Required(u'必填项'), Length(1, 200)])
    apply_profession = StringField(u'申请专业', validators=[Required(u'必填项'), Length(1, 400)])
    submit = SubmitField(u'报名')

    def validate_mobile(self, field):
        if Apply.query.filter_by(mobile=field.data).first():
            raise ValidationError(u'该手机号码已报名.')

    def validate_id_card(self, field):
        if Apply.query.filter_by(id_card=field.data).first():
            raise ValidationError(u'该身份证号已报名.')

    def validate_ticket_number(self, field):
        if Apply.query.filter_by(ticket_number=field.data).first():
            raise ValidationError(u'该准考证号已报名.')


class EditApplyForm(Form):
    apply_id = StringField(u'报名编号', validators=[Required(u'必填项')])
    real_name = StringField(u'真实姓名', validators=[Required(u'必填项'), Length(1, 64)])
    mobile = StringField(u'手机号码', validators=[Required(u'必填项'), Length(11, 11, u'请填写正确的手机号码')])
    id_card = StringField(u'身份证号', validators=[Required(u'必填项'), Length(18, 18, u'请填写正确的身份证号')])
    point = IntegerField(u'高考分数', validators=[Required(u'必填项')])
    ticket_number = StringField(u'准考证号', validators=[Required(u'必填项'), Length(1, 200)])
    apply_profession = StringField(u'申请专业', validators=[Required(u'必填项'), Length(1, 400)])
    apply_time = DateTimeField(u'申请时间')
    status = SelectField(
        u'报名状态',
        choices=[(u'新申请', u'新申请'), (u'已处理', u'已处理')]
    )
    submit = SubmitField(u'修改')
    close = SubmitField(u'关闭')

    def __init__(self, *args, **kwargs):
        super(EditApplyForm, self).__init__(*args, **kwargs)
        read_only(self.apply_id)
        read_only(self.apply_time)

    def validate_mobile(self, field):
        if Apply.query.filter_by(mobile=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该手机号码已报名.')

    def validate_id_card(self, field):
        if Apply.query.filter_by(id_card=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该身份证号已报名.')

    def validate_ticket_number(self, field):
        if Apply.query.filter_by(ticket_number=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该准考证号已报名.')


class EditApplyAdminForm(Form):
    apply_id = StringField(u'报名编号', validators=[Required(u'必填项')])
    real_name = StringField(u'真实姓名', validators=[Required(u'必填项'), Length(1, 64)])
    mobile = StringField(u'手机号码', validators=[Required(u'必填项'), Length(11, 11, u'请填写正确的手机号码')])
    id_card = StringField(u'身份证号', validators=[Required(u'必填项'), Length(18, 18, u'请填写正确的身份证号')])
    point = IntegerField(u'高考分数', validators=[Required(u'必填项')])
    ticket_number = StringField(u'准考证号', validators=[Required(u'必填项'), Length(1, 200)])
    apply_profession = StringField(u'申请专业', validators=[Required(u'必填项'), Length(1, 400)])
    apply_time = DateTimeField(u'申请时间')
    status = SelectField(
        u'报名状态',
        choices=[(u'新申请', u'新申请'), (u'已处理', u'已处理')]
    )
    submit = SubmitField(u'修改')
    close = SubmitField(u'关闭')

    def __init__(self, *args, **kwargs):
        super(EditApplyAdminForm, self).__init__(*args, **kwargs)
        read_only(self.apply_id)

    def validate_mobile(self, field):
        if Apply.query.filter_by(mobile=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该手机号码已报名.')

    def validate_id_card(self, field):
        if Apply.query.filter_by(id_card=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该身份证号已报名.')

    def validate_ticket_number(self, field):
        if Apply.query.filter_by(ticket_number=field.data).filter(Apply.id != self.apply_id.data).first():
            raise ValidationError(u'该准考证号已报名.')
