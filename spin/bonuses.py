from flask import flash

from models import db
from settings import (
    LOGIN_BONUS_AMOUNT, DEPOSIT_BONUS_AMOUNT, DEPOSIT_BONUS_CONDITION
)


def login_bonus(user):
    user.eur_account.balance += LOGIN_BONUS_AMOUNT
    db.session.add(user)
    db.session.commit()
    flash('You were awarded 100 EUR!')


def deposit_bonus(user, amount):
    if amount > DEPOSIT_BONUS_CONDITION:
        user.bns_account.balance += DEPOSIT_BONUS_AMOUNT
        db.session.add(user)
        db.session.commit()
        flash('You were awarded {0} BNS'.format(
            round(DEPOSIT_BONUS_AMOUNT, 2)))
