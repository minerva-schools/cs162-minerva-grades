import forum_fetcher
import unittest
class LoTest(unittest.TestCase):
    def test_lo_fetch(self):
        fetcher = forum_fetcher.LoFetcher("4vht0a8arc3gowc8cr8j4ww654voh3fi")
        out = fetcher.get_grades()
        with open('los.txt', 'w', encoding='utf-8') as outfile:
            outfile.write(str(out[0]))
        with open('lo_grades.txt', 'w', encoding='utf-8') as outfile:
            outfile.write(str(out[1]))
    def test_hc_fetch(self):
        fetcher = forum_fetcher.HcFetcher("4vht0a8arc3gowc8cr8j4ww654voh3fi")
        out = fetcher.get_grades()
        with open('hcs.txt', 'w', encoding='utf-8') as outfile:
            outfile.write(str(out[0]))
        with open('hc_grades.txt', 'w', encoding='utf-8') as outfile:
            outfile.write(str(out[1]))

if __name__ == "__main__":
    unittest.main()