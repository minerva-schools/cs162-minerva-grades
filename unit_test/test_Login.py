from flask_testing import TestCase
from dashboard import app, db
from dashboard.models import User
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
import unittest
from dotenv import load_dotenv
from flask_login import login_user, current_user, logout_user, login_required
import os

load_dotenv()
# To run this, set the environment variable SESSION_ID to your Forum session id
session_id = os.environ.get("SESSION_ID")

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestBasic(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        assert response.status_code == 200

    # Ensure that dashboard page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

'''

class TestLogin(BaseTestCase):
   
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(user_id="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Login unsuccessful. Please check Session ID.', response.data)
    

    
    def test_correct_login(self):
        with self.client:
            response0 = self.client.post('/login',
                data=dict(user_id=session_id),
                follow_redirects=True
            )
            response = self.client.get('/dashboard', follow_redirects=True)
            print(response.status_code, response.data)
            timer = 0
            while response0.status_code == 200:
                time.sleep(5)
                timer += 5
                print("waiting", response.status_code, timer)
                if timer > 200:
                    break
                if response.status_code == 302:
                    break
            print(response.status_code, response.data)
            self.assertIn(b'Hi, you have been logged in.', response.data)
            self.assertTrue(current_user.user_id == session_id)
            self.assertTrue(current_user.is_active())

'''

if __name__ == '__main__':
    unittest.main()

