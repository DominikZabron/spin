import random

from settings import BET_AMOUNT, WIN_AMOUNT
from utils import collect_bet, pay_out_win


def draw():
    """Simulate 3 independent random numbers and return them."""
    def n(): return random.randint(0, 2)
    return n(), n(), n()


def game(user):
    """Return random numbers representing each monkey types.

    Take into account bet collecting and distributing wins when happened.
    Otherwise if accounts are empty return False.
    """
    currency = collect_bet(user, amount=BET_AMOUNT)
    if currency:
        deal = draw()
        if deal in ((0, 0, 0), (1, 1, 1), (2, 2, 2)):
            pay_out_win(user, currency, BET_AMOUNT, WIN_AMOUNT)
    else:
        return False
    return deal
