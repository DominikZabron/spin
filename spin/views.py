from flask_login import LoginManager, login_required

from spin import app
from models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
@login_required
def play():
    return ''
