from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class LoginForm(FlaskForm):
    sessionID = StringField('Session ID')
    submit = SubmitField('Login')


class DropDownList(FlaskForm):
    course = SelectField('course', choices=[])
