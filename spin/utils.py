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


def collect_bet(user, amount):
    if user.eur_account.balance >= amount:
        user.eur_account.balance -= amount
        currency = 'EUR'
    elif user.bns_account.balance >= amount:
        user.bns_account.balance -= amount
        currency = 'BNS'
    else:
        flash('Your accounts are empty. '
              'You need to deposit more money to play.')
        return False
    db.session.add(user)
    db.session.commit()
    return currency


def pay_out_win(user, currency, bet, win):
    if currency == 'EUR':
        user.eur_account.balance += bet + win
        flash('Congratulations! You won {0} EUR.'.format(win))
    elif currency == 'BNS':
        user.bns_account.balance += bet + win
        flash('Congratulations! You won {0} BNS.'.format(win))
    else:
        flash('Error. Unrecognized currency.')
    db.session.add(user)
    db.session.commit()
