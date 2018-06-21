import json
import unittest
from app.models import User, UserType


class BaseTest(unittest.TestCase):
    """This will hold the basic methods required by other tests, for
    example authentication in order to test guarded endpoints
    """

    def setUpAuth(self):
        """Setup user authentication headers for use during tests"""
        self.user, self.user_headers = self.authUser()
        self.admin, self.admin_headers = self.authAdmin()

    def authAdmin(self, email='admin@mail.com'):
        """Create and authenticate an admin user"""
        admin = self._createUser(email=email, role=UserType.ADMIN)
        return admin, self._authenticate(admin)

    def authUser(self, email='user@mail.com'):
        """Create and authenticate a normal user"""
        user = self._createUser(email=email, role=UserType.USER)
        return user, self._authenticate(user)

    def _createUser(self, email, role):
        """Creates a user with given mail and role"""
        with self.app.app_context():
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    name='John',
                    email=email, 
                    password='secret',
                    role=role
                )
                user.save()
            return user
        
    def _authenticate(self, user):
        """Authenticates a user and returns the auth headers"""
        res = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': user.email,
                'password': user.password
            }),
            headers={'Content-Type' : 'application/json'}
        )
        result = json.loads(res.get_data(as_text=True))
        return {
            'Content-Type' : 'application/json',
            'Authorization': 'Bearer {}'.format(result['access_token'])
        }

