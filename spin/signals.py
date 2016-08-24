from bonuses import login_bonus


def apply_login_bonus(sender, user, **extra):
    login_bonus(user)
