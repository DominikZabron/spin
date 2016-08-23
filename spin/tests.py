from flask import url_for

from flask_testing import TestCase

from spin import app
from models import db, User
from settings import TEST_DB_URI


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
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_index_no_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.login('name', 'pass')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_index_with_login(self):
        self.login('name', 'pass')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_logout(self):
        self.login('name', 'pass')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')

    def test_login_bad_name(self):
        response = self.login('bad_name', 'pass')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')

    def test_login_bad_pass(self):
        response = self.login('name', 'bad_pass')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('login.html')
