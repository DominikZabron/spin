from flask import render_template, flash, redirect, url_for, request

from flask_login import (
    LoginManager, login_required, login_user, logout_user, user_logged_in,
    current_user
)

from spin import app
from models import User
from forms import LoginForm, RegisterForm, DepositForm
from models import db
from signals import apply_login_bonus
from utils import transfer_deposit
from game import game

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

user_logged_in.connect(apply_login_bonus)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
@login_required
def play():
    choices = (
        request.args.get('a', 0),
        request.args.get('b', 1),
        request.args.get('c', 2)
    )
    return render_template('index.html', form=DepositForm(), choices=choices)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('play'))
            else:
                flash('Wrong password.')
        else:
            flash('Username does not exist.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            user = User.query.filter(User.username == form.username.data).first()
            if user:
                flash('Username already exists.')
            else:
                user = User(form.username.data, form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('play'))
        else:
            flash('Passwords do not match.')
    return render_template('register.html', form=form)


@app.route('/deposit', methods=['POST'])
def deposit():
    form = DepositForm()
    if form.validate_on_submit():
        amount = form.amount.data
        transfer_deposit(current_user, amount)
    return redirect(url_for('play'))


@app.route('/spin')
def spin():
    deal = game(current_user)
    if deal:
        return redirect(url_for('play', a=deal[0], b=deal[1], c=deal[2]))
    else:
        return redirect(url_for('play'))
