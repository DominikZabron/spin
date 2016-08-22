from flask_testing import TestCase

from spin import app


class SpinTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
