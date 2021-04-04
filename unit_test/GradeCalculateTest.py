import unittest
from __init__ import db
from models import Hc, Lo, HcGrade, LoGrade


class GradeCalculateTest(TestCase):

    def test_calculate_co_score(self, co_id):
        co_score = calculate_co_score(co_id)
        self.assertEqual(co_score, #)
    
    def test_calculate_course_score(self, course):
        course_score = calculate_course_score(course)
        self.assertEqual(course_score, #)
    
    def test_calculate_gpa(self):
        gpa = calculate_gpa()
        self.assertEqual(gpa, #)
    
    def test_least_frequent_Lo(self):
        least_freq_Lo = least_Lo()
        self.assertEqual(least_freq_Lo, #)
    
    def least_frequent_Hc(self):
        least_freq_Lo = least_Hc()
        self.assertEqual(least_frequent_Hc, #)

if __name__ == "__main__":
    unittest.main()