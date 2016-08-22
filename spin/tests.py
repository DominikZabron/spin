from flask_testing import TestCase

from spin import app
from models import db, User
from settings import TEST_DB_URI


class SpinTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        return app

    def setUp(self):
        db.create_all()
        self.user = User('name', 'pass')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 401)
