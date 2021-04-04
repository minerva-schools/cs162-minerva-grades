import unittest
from __init__ import db
from models import Hc, Lo, HcGrade, LoGrade


class GradeCalculateTest(TestCase):

    def test_calculate_co_score(self, co_id):
        co_score = calculate_co_score(co_id)
        assert(co_score != 0)
    
    def test_calculate_course_score(self, course):
        course_score = calculate_course_score(course)
        assert(course_score != 0)
    
    def test_calculate_gpa(self):
        gpa = calculate_gpa()
        assert(gpa != 0)
    
    def test_least_frequent_Lo(self):
        least_freq_Lo = least_Lo()
        assert(least_freq_Lo != 0)
    
    def least_frequent_Hc(self):
        least_freq_Lo = least_Hc()
        assert(least_frequent_Hc != 0)

if __name__ == "__main__":
    unittest.main()