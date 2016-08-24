from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import PasswordInput


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField(
        'password',
        validators=[DataRequired()],
        widget=PasswordInput()
    )


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField(
        'password',
        validators=[DataRequired()],
        widget=PasswordInput()
    )
    password2 = StringField(
        'confirm password',
        validators=[DataRequired()],
        widget=PasswordInput()
    )


class DepositForm(Form):
    amount = DecimalField(
        'amount',
        validators=[DataRequired(), NumberRange(0, 1000000)],
        places=12,
        rounding=2
    )
