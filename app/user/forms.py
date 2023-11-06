from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class UserRegistrationForm(FlaskForm):
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField(label="Repeat Password", validators=[DataRequired(), Length(min=8)])
