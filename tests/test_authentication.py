
import json
import unittest
from app import create_app, db
from app.models import User, UserType

class AuthenticationTestCase(unittest.TestCase):
    """This will test authentication endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.user = json.dumps({
            'username': 'John',
            'email': 'john@doe.com',
            'password': 'secret',
            'confirm_password': 'secret'
        })
        self.headers = {'Content-Type' : 'application/json'}
        with self.app.app_context():
            db.create_all()

