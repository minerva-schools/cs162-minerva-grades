import unittest
from dashboard import db, app
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
import pandas as pd
from dashboard.grade_calculations import Co_grade_query, calc_course_grade, co_grade_over_time, hc_grade_over_time, single_hc_wavg
from sqlalchemy import cast, Float, func, case

import datetime
"""
class HCGradeCalculationTest(unittest.TestCase):

    def setUp(self):
        app.config.update(TESTING=True)
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

        db.create_all()
        db.session.commit()

        session_id = "ku83chpu36xj0z24cu9qqtvqrkhlghwm"
        fetcher = HcFetcher(session_id)
        fetcher.get_grades()

        db.session.commit()

    def test_hc_grade_over_time(self):
        session_id = "ku83chpu36xj0z24cu9qqtvqrkhlghwm"
        # test the function of hc_grade_over_time
        result = hc_grade_over_time(session_id, 'CS')
        self.assertEqual(result.iloc[0][0], '2019-09-12')
        self.assertEqual(result.iloc[1][1], 3.0)

    def test_single_hc_wavg(self):
        # test the function of single_hc_wavg
        result = single_hc_wavg(user_id='ku83chpu36xj0z24cu9qqtvqrkhlghwm', HcName='interpretivelens')
        self.assertEqual(result.iloc[-1][1], 6.0)

    def tearDown(self):
        db.drop_all()
        self.context.pop()
"""