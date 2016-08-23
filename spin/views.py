from flask import render_template, flash, redirect, url_for

from flask_login import LoginManager, login_required, login_user, logout_user

from spin import app
from models import User
from forms import LoginForm
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
    return redirect('login')
