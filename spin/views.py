from flask import render_template, flash, redirect, url_for

from flask_login import LoginManager, login_required, login_user, logout_user

from spin import app
from models import User
from forms import LoginForm, RegisterForm
from models import db

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
@login_required
def play():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=True)

                flash('Logged in successfully.')
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
