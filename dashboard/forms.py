from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

class LoginForm(FlaskForm):
    sessionID = StringField('Session ID')
    submit = SubmitField('Login')