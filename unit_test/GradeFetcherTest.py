import forum_fetcher
import unittest
from web.serve import db

session_id = ""
class FetcherTest(unittest.TestCase):

    def test_lo_fetch(self):
        fetcher = forum_fetcher.LoFetcher(session_id)
        fetcher.get_grades()
    def test_hc_fetch(self):
        fetcher = forum_fetcher.HcFetcher(session_id)
        fetcher.get_grades()

if __name__ == "__main__":
    unittest.main()