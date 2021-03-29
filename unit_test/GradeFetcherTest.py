import forum_fetcher
import unittest
from web.serve import db, Lo, LoGrade, Hc,HcGrade

session_id = "4vht0a8arc3gowc8cr8j4ww654voh3fi"
class FetcherTest(unittest.TestCase):

    def test_lo_fetch(self):
        fetcher = forum_fetcher.LoFetcher(session_id)
        fetcher.get_grades()
        assert db.session.query(Lo).filter_by(user_id=session_id).first()
        assert db.session.query(LoGrade).filter_by(user_id=session_id).first()
    def test_hc_fetch(self):
        fetcher = forum_fetcher.HcFetcher(session_id)
        fetcher.get_grades()
        assert db.session.query(Hc).filter_by(user_id=session_id).first()
        assert db.session.query(HcGrade).filter_by(user_id=session_id).first()

if __name__ == "__main__":
    unittest.main()