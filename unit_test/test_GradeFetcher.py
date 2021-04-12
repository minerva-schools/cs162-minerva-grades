import os
import unittest
from dashboard import db
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
from dotenv import load_dotenv

load_dotenv()
# To run this, set the environment variable SESSION_ID to your Forum session id
session_id = os.environ.get("SESSION_ID")
class FetcherTest(unittest.TestCase):

    def test_lo_fetch(self):
        """Test fetching LOs"""
        print(session_id)
        fetcher = LoFetcher(session_id)
        fetcher.get_grades()
        # Test that database was filled
        assert db.session.query(Lo).filter_by(user_id=session_id).first()
        assert db.session.query(LoGrade).filter_by(user_id=session_id).first()
    def test_hc_fetch(self):
        """Test fetching Hcs"""
        fetcher = HcFetcher(session_id)
        fetcher.get_grades()
        # Test that database was filled
        assert db.session.query(Hc).filter_by(user_id=session_id).first()
        assert db.session.query(HcGrade).filter_by(user_id=session_id).first()

if __name__ == "__main__":
    unittest.main()