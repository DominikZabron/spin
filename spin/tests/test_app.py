from mock import Mock, patch

from flask import url_for

from flask_testing import TestCase

from spin import app
from ..models import db, User
from ..settings import (
    TEST_DB_URI, LOGIN_BONUS_AMOUNT, DEPOSIT_BONUS_AMOUNT,
    DEPOSIT_BONUS_CONDITION, BET_AMOUNT, WIN_AMOUNT
)


class SpinTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self.user = User('name', 'pass')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post(url_for('login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('logout'), follow_redirects=True)

    def test_index_no_login(self):
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.login('name', 'pass')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_index_with_login(self):
        self.login('name', 'pass')
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_logout(self):
        self.login('name', 'pass')
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 200)
        self.logout()
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')

    def test_login_bad_name(self):
        response = self.login('bad_name', 'pass')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')

    def test_login_bad_pass(self):
        response = self.login('name', 'bad_pass')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url_for('play'))
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')

    def test_register_user(self):
        username, password = 'new_name', 'new_pass'
        response = self.client.post(url_for('register'), data=dict(
            username=username,
            password=password,
            password2=password
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_register_username_exists(self):
        username, password = 'new_name', 'new_pass'
        response = self.client.post(url_for('register'), data=dict(
            username=self.user.username,
            password=password,
            password2=password
        ))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')

    def test_register_passwords_not_match(self):
        username, password = 'new_name', 'new_pass'
        response = self.client.post(url_for('register'), data=dict(
            username=username,
            password=password,
            password2='other_pass'
        ))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')

    def test_login_add_bonus(self):
        prev_balance = self.user.eur_account.balance
        response = self.login('name', 'pass')
        self.assertEqual(response.status_code, 200)
        new_balance = self.user.eur_account.balance
        self.assertEqual(new_balance, prev_balance + LOGIN_BONUS_AMOUNT)

    def test_deposit(self):
        self.login('name', 'pass')
        prev_balance = self.user.eur_account.balance
        deposit_amount = 22
        response = self.client.post(url_for('deposit'), data=dict(
            amount=deposit_amount
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
        db.session.refresh(self.user)
        new_balance = self.user.eur_account.balance
        self.assertEqual(new_balance, prev_balance + deposit_amount)

    def test_deposit_with_bonus(self):
        self.login('name', 'pass')
        prev_balance = self.user.bns_account.balance
        deposit_amount = DEPOSIT_BONUS_CONDITION + 1
        self.client.post(url_for('deposit'), data=dict(
            amount=deposit_amount
        ), follow_redirects=True)
        db.session.refresh(self.user)
        new_balance = self.user.bns_account.balance
        self.assertEqual(new_balance, prev_balance + DEPOSIT_BONUS_AMOUNT)

    def test_deposit_without_bonus(self):
        self.login('name', 'pass')
        prev_balance = self.user.bns_account.balance
        deposit_amount = DEPOSIT_BONUS_CONDITION - 1
        self.client.post(url_for('deposit'), data=dict(
            amount=deposit_amount
        ), follow_redirects=True)
        db.session.refresh(self.user)
        new_balance = self.user.bns_account.balance
        self.assertEqual(new_balance, prev_balance)

    @patch('spin.game.draw')
    def test_win(self, draw_mock):
        draw_mock.return_value = (0, 0, 0)
        self.login('name', 'pass')
        prev_value = self.user.eur_account.balance
        response = self.client.get(url_for('spin'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location.split('/')[-1], '?a=0&c=0&b=0')
        new_value = self.user.eur_account.balance
        self.assertEqual(new_value, prev_value + WIN_AMOUNT)

    @patch('spin.game.draw')
    def test_loose(self, draw_mock):
        draw_mock.return_value = (2, 1, 0)
        self.login('name', 'pass')
        prev_value = self.user.eur_account.balance
        response = self.client.get(url_for('spin'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location.split('/')[-1], '?a=2&c=0&b=1')
        new_value = self.user.eur_account.balance
        self.assertEqual(new_value, prev_value - BET_AMOUNT)

    @patch('spin.game.draw')
    def test_win_bonus(self, draw_mock):
        draw_mock.return_value = (1, 1, 1)
        self.login('name', 'pass')
        self.user.eur_account.balance = 0
        self.user.bns_account.balance = 100
        response = self.client.get(url_for('spin'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location.split('/')[-1], '?a=1&c=1&b=1')
        new_value = self.user.bns_account.balance
        self.assertEqual(new_value, 100 + WIN_AMOUNT)

    @patch('spin.game.draw')
    def test_loose_bonus(self, draw_mock):
        draw_mock.return_value = (0, 1, 2)
        self.login('name', 'pass')
        self.user.eur_account.balance = 0
        self.user.bns_account.balance = 100
        response = self.client.get(url_for('spin'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location.split('/')[-1], '?a=0&c=2&b=1')
        new_value = self.user.bns_account.balance
        self.assertEqual(new_value, 100 - BET_AMOUNT)

    def test_empty_account(self):
        self.login('name', 'pass')
        self.user.eur_account.balance = 0
        self.user.bns_account.balance = 0
        response = self.client.get(url_for('spin'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.eur_account.balance, 0)
        self.assertEqual(self.user.bns_account.balance, 0)
