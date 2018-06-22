import json
from app import create_app, db
from app.models import User, UserType
from .base import BaseTest

class TestMeals(BaseTest):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.setUpAuth()

    def data(self):
        return json.dumps({
            'name': 'ugali',
            'cost': 30.0
        })

    def test_can_create_meal(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data(),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Successfully saved meal', res.data)

    def test_cannot_create_meal_without_cost(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data_without(['cost']),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'cost field is required', res.data)

    def test_cannot_create_meal_without_name(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data_without(['name']),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'name field is required', res.data)

    def test_cannot_create_meal_without_numeric_cost(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data_with({'cost': 'xxx'}),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'cost must be a positive number', res.data)

    def test_cannot_create_meal_without_positive_cost(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data_with({'cost': -20}),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'cost must be a positive number', res.data)

    def test_cannot_create_meal_without_unique_name(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data(),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Successfully saved meal', res.data)
        res = self.client.post(
            'api/v1/meals',
            data=self.data_with({'name': 'Ugali'}),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'The name is already taken', res.data)

    def test_can_get_meal(self):
        res = self.client.post(
            'api/v1/meals',
            data=self.data(),
            headers=self.admin_headers
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Successfully saved meal', res.data)
        json_res = self.to_json(res)['data']
        res = self.client.get(
            'api/v1/meals/{}'.format(json_res['meal']['id']),
            data=self.data(),
            headers=self.user_headers
        )
        json_res = self.to_json(res)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
