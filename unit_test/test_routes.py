import os
import unittest
from dashboard import db
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
from dotenv import load_dotenv
load_dotenv()
# To run this, set the environment variable SESSION_ID to your Forum session id
session_id = os.environ.get("SESSION_ID")

class RoutesTests(unittest.TestCase):
    def test_something(self):
        """

        """
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
