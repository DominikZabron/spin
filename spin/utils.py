from flask import flash

from models import db
from bonuses import deposit_bonus


def transfer_deposit(user, amount):
    user.eur_account.balance += amount
    db.session.add(user)
    db.session.commit()
    flash('You have successfully deposited {0} EUR'.format(
        round(amount, 2)))
    deposit_bonus(user, amount)
