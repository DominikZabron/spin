from flask import flash

from settings import LOGIN_BONUS_AMOUNT
from models import db


def apply_login_bonus(sender, user, **extra):
    user.eur_account.balance += LOGIN_BONUS_AMOUNT
    db.session.add(user)
    db.session.commit()
    flash('You were awarded 100 EUR!')
