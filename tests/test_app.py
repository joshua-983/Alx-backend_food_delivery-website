import sys
import os
import unittest
import json
from application import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Our Food Delivery Service', response.data)

    def test_get_menu(self):
        response = self.app.get('/menu')
        self.assertEqual(response.status_code, 200)
        menu = json.loads(response.data)
        self.assertEqual(len(menu), 4)  # Check if we have 4 items

    def test_get_menu_search(self):
        response = self.app.get('/menu?search=burger')
        self.assertEqual(response.status_code, 200)
        menu = json.loads(response.data)
        self.assertEqual(len(menu), 1)
        self.assertEqual(menu[0]['name'], 'Burger')

    def test_submit_contact(self):
        contact_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "message": "Hello!"
        }
        response = self.app.post('/submit_contact',
                                 data=json.dumps(contact_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for contacting us!', response.data)

    def test_signup(self):
        signup_data = {
            "username": "johndoe",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.app.post('/signup',
                                 data=json.dumps(signup_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up successful!', response.data)

    def test_login_success(self):
        signup_data = {
            "username": "johndoe",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        self.app.post('/signup',
                      data=json.dumps(signup_data),
                      content_type='application/json')

        login_data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.app.post('/login',
                                 data=json.dumps(login_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_failure(self):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = self.app.post('/login',
                                 data=json.dumps(login_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password!', response.data)

if __name__ == '__main__':
    unittest.main()

