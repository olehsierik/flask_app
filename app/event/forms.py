from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from datetime import datetime


def date_greater_than_today(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('The date must be greater than today.')


def date_end_greater_than_start(form, field):
    start_date = form.begin_at.data
    end_date = field.data

    if end_date <= start_date:
        raise ValidationError('The end date must be greater than the start date.')


class EventForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(), Length(min=5)])
    description = StringField(label='Description', validators=[DataRequired()])
    begin_at = DateField(label='Date start', validators=[DataRequired(), date_greater_than_today])
    end_at = DateField(label='Date end',
                       validators=[DataRequired(), date_greater_than_today, date_end_greater_than_start])
    max_users = IntegerField(label='Max participants', validators=[DataRequired(), NumberRange(min=1,
                                                                                               message='The value must be greater than 0')])
    is_active = BooleanField(label='Active')
