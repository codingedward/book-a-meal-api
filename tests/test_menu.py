import json
from app import create_app, db
from app.models import User, UserType
from .base import BaseTest

class TestMenu(BaseTest):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.setUpAuth()

    def data(self):
        return json.dumps({
            'name': 'Lunch'
        })

    def test_can_create_menu(self):
        res = self.client.post(
            'api/v1/menus',
            data=self.data(),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Successfully saved menu', res.data)

    def test_cannot_create_menu_without_name(self):
        res = self.client.post(
            'api/v1/menus',
            data=self.data_without(['name']),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'name field is required', res.data)

    def test_can_get_menu(self):
        self.create_menu(self.data())
        res = self.client.get(
            'api/v1/menus',
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Lunch', res.data)


    def create_menu(self, data):
        res = self.client.post(
            'api/v1/menus',
            data=data,
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Successfully saved menu', res.data)


