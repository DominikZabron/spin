from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password',
                           validators=[DataRequired()], widget=PasswordInput())
