import unittest
from dashboard import db
from dashboard.models import Lo, LoGrade, Hc, HcGrade
import pandas as pd
from dashboard.grade_calculations import Co_grade_query, calc_course_grade, co_grade_over_time
from sqlalchemy import cast, Float, func, case

import datetime

class GradeCalculationTest(unittest.TestCase):

    def setUp(self):
        db.create_all()
        # add fictious data
        gradesample = [
            (
            1221103, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 7, 14, 28, 34), False),
            (1221261, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 8, 19, 7, 13), False),
            (1221459, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 9, 14, 32, 24), False),
            (
            1221472, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 9, 14, 59, 48), False),
            (
            1221834, 9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2020, 9, 10, 17, 59, 27), False),
            (1223894, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 14, 19, 42, 18),
             False),
            (1224478, 9863, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 15, 19, 1, 49), False),
            (
            1225059, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 16, 18, 25, 42), False),
            (1225673, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 17, 21, 4, 55), False),
            (
            1226360, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 18, 17, 48, 39), False),
            (1226983, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 19, 16, 36, 6), True),
            (1227058, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 19, 18, 0, 39), True),
            (1227071, 9947, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 19, 18, 5, 17), False),
            (1228613, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 21, 21, 13, 22),
             False),
            (
            1229576, 9863, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2020, 9, 23, 10, 19, 57), False),
            (1229691, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 23, 12, 4, 58), False),
            (
            1230564, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 24, 15, 53, 48), False),
            (
            1231515, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 25, 12, 39, 43), True),
            (
            1231559, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 25, 13, 47, 34), True),
            (
            1231560, 10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 25, 13, 47, 37), True),
            (1231693, 9941, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 25, 15, 27, 6), False),
            (
            1232797, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 26, 14, 22, 21), True),
            (1233539, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 9, 26, 23, 4, 37), False),
            (
            1233943, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 9, 27, 14, 24, 10), True),
            (1236064, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 29, 16, 36, 21),
             False),
            (
            1236103, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 29, 17, 0, 42), False),
            (
            1236564, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 9, 30, 10, 13, 37), False),
            (
            1237408, 9862, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 1, 18, 29, 27), False),
            (
            1238783, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 2, 20, 36, 30), True),
            (
            1238784, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 2, 20, 36, 41), True),
            (1240843, 9940, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 4, 8, 31, 52), True),
            (
            1241344, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 1, 1, datetime.datetime(2020, 10, 4, 17, 55, 25), False),
            (1241665, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 4, 21, 42, 21), True),
            (
            1243080, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 6, 19, 29, 32), False),
            (1243164, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 6, 21, 18, 20),
             False),
            (1243181, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 6, 21, 28, 59),
             False),
            (1244036, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 7, 19, 24, 35), True),
            (1245398, 9864, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 9, 14, 1, 44), False),
            (
            1246602, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 10, 9, 45, 34), True),
            (1246603, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 10, 9, 46), True),
            (
            1247694, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 11, 1, 56, 26), False),
            (1247819, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 11, 2, 54, 4), False),
            (1248654, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 11, 17, 14, 21),
             False),
            (1250163, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 12, 16, 17, 31),
             False),
            (1250950, 9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 10, 12, 21, 8, 34), True),
            (
            1250958, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 10, 12, 21, 12, 47), True),
            (1250980, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 10, 12, 21, 22, 7), True),
            (
            1250982, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 10, 12, 21, 23, 14), True),
            (
            1250983, 9863, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 10, 12, 21, 23, 49), True),
            (
            1250984, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 10, 12, 21, 24, 38), True),
            (1254127, 9864, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 15, 17, 54, 51),
             False),
            (1257294, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 18, 18, 26, 2),
             False),
            (1257345, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 18, 19, 13, 46),
             True),
            (1257349, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 18, 19, 14, 32),
             True),
            (1257497, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 18, 21, 51, 14),
             False),
            (1257760, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 10, 19, 1, 32, 6), True),
            (
            1257761, 10101, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 10, 19, 1, 32, 55), True),
            (
            1257762, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 1, 3, datetime.datetime(2020, 10, 19, 1, 33, 36), True),
            (1259571, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 20, 20, 5, 7), False),
            (1260977, 9864, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 22, 14, 53, 32),
             False),
            (1262248, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 10, 23, 15, 12, 22),
             False),
            (
            1264112, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 2, datetime.datetime(2020, 10, 24, 19, 27, 2), True),
            (1268111, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 27, 21, 32, 54),
             True),
            (1268113, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 27, 21, 33, 42),
             True),
            (1269035, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 28, 17, 37, 18),
             False),
            (1269551, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 28, 23, 10, 51),
             False),
            (
            1269654, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2020, 10, 29, 0, 53, 7), False),
            (1270381, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 10, 29, 20, 26, 35),
             False),
            (
            1272407, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 10, 31, 13, 2, 22), True),
            (1274176, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 2, 0, 7, 43), True),
            (1274178, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 3, datetime.datetime(2020, 11, 2, 0, 8, 35), True),
            (1274180, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 2, 0, 9, 56), True),
            (1274182, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 2, 0, 10, 23), True),
            (1274185, 10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 2, 0, 10, 56), True),
            (1274826, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 2, datetime.datetime(2020, 11, 2, 15, 14, 7), True),
            (1274869, 9862, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 11, 2, 16, 0, 6), True),
            (1274886, 9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 2, datetime.datetime(2020, 11, 2, 16, 9, 46), True),
            (1274921, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 2, datetime.datetime(2020, 11, 2, 17, 17, 50), True),
            (1274923, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 2, datetime.datetime(2020, 11, 2, 17, 18, 15), True),
            (
            1277562, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 4, 19, 14, 11), False),
            (1279184, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 6, 13, 59, 8), False),
            (1284087, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 9, 20, 2, 3), False),
            (
            1284431, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 10, 1, 6, 11), False),
            (1284461, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 10, 1, 15, 37),
             False),
            (1284652, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 10, 2, 8, 45), False),
            (1285425, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 10, 19, 14, 47),
             False),
            (1285520, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 10, 19, 46, 52),
             False),
            (1286629, 9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 11, 10, 23, 37),
             False),
            (1287710, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 11, 23, 49, 52),
             False),
            (1288491, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 12, 18, 31, 32),
             False),
            (1290927, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2020, 11, 14, 18, 26), False),
            (1290992, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 14, 18, 55, 43),
             False),
            (1291132, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 14, 19, 22, 53),
             False),
            (1291519, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 14, 21, 13, 14),
             False),
            (
            1292298, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 2, datetime.datetime(2020, 11, 15, 12, 5, 28), True),
            (
            1292568, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 4, datetime.datetime(2020, 11, 15, 16, 13, 50), True),
            (
            1292571, 9945, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 11, 15, 16, 14, 34), True),
            (1294355, 9940, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 16, 6, 41, 39), True),
            (1294357, 9940, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 16, 6, 43, 6), True),
            (
            1296179, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 4, datetime.datetime(2020, 11, 17, 19, 50, 58), True),
            (
            1296180, 9945, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 11, 17, 19, 52, 32), True),
            (1297021, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 18, 15, 18, 43),
             False),
            (1297412, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 18, 20, 7, 37), True),
            (1297413, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 18, 20, 8, 8), True),
            (1297421, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 11, 18, 20, 14), True),
            (
            1297422, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 11, 18, 20, 14, 39), True),
            (1299880, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 20, 16, 17, 39),
             False),
            (1301460, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 11, 21, 13, 42, 29),
             True),
            (1301587, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 11, 21, 14, 59, 47),
             True),
            (1304441, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2020, 11, 22, 22, 42, 11),
             False),
            (1304685, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 22, 23, 42, 31),
             False),
            (
            1307153, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 11, 24, 19, 6, 18), True),
            (
            1307240, 9866, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 11, 24, 20, 9, 43), False),
            (1308721, 10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 25, 17, 46, 37),
             True),
            (1308724, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 11, 25, 17, 47, 35),
             True),
            (1308729, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 11, 25, 17, 48, 15),
             True),
            (1308733, 10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 11, 25, 17, 49, 17),
             True),
            (
            1308990, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 11, 25, 20, 9, 41), True),
            (
            1310397, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 26, 19, 15, 4), False),
            (1310650, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 11, 26, 22, 17, 54),
             False),
            (
            1316441, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 30, 16, 49, 35), True),
            (
            1316443, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 11, 30, 16, 49, 55), True),
            (
            1316736, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2020, 11, 30, 19, 58, 38), True),
            (
            1316737, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2020, 11, 30, 19, 58, 48), True),
            (1316748, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 6, datetime.datetime(2020, 11, 30, 20, 3, 59), True),
            (1316765, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 6, datetime.datetime(2020, 11, 30, 20, 9, 26), True),
            (1316766, 9862, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2020, 11, 30, 20, 9, 47), True),
            (1317227, 10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 12, 1, 1, 52, 17), True),
            (
            1318573, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 2, 2, 57, 18), False),
            (
            1320901, 9862, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 3, 19, 44, 47), False),
            (1323243, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2020, 12, 6, 11, 33, 15), True),
            (1323245, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 12, 6, 11, 34, 20), True),
            (1323246, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 12, 6, 11, 36, 39), True),
            (1323731, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 7, 0, 50, 51), False),
            (1324055, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 12, 7, 5, 19, 29), False),
            (1324189, 9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 12, 7, 5, 45, 9), False),
            (1325227, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 12, 7, 21, 52, 44), True),
            (1326187, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 12, 8, 19, 0, 26), True),
            (1326253, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2020, 12, 8, 21, 26, 46), True),
            (
            1326659, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 2, datetime.datetime(2020, 12, 9, 15, 34, 21), True),
            (1327593, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 2, datetime.datetime(2020, 12, 10, 12, 59, 15),
             True),
            (1328901, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 12, 12, 11, 52, 27),
             False),
            (1329545, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 10, datetime.datetime(2020, 12, 12, 19, 14, 32),
             True),
            (1329546, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 10, datetime.datetime(2020, 12, 12, 19, 14, 43),
             True),
            (1329547, 10101, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 10, datetime.datetime(2020, 12, 12, 19, 14, 51),
             True),
            (1332240, 9945, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 14, 5, 5, 19), True),
            (
            1332909, 9947, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 14, 16, 39, 40), True),
            (
            1332910, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 14, 16, 40, 17), True),
            (1332915, 9940, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2020, 12, 14, 16, 42, 9), True),
            (1338706, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 18, 13, 57), False),
            (1338760, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 18, 14, 21, 45),
             False),
            (1339059, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2020, 12, 18, 18, 32, 18),
             False),
            (
            1339626, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2020, 12, 19, 0, 48, 13), False),
            (
            1343712, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 21, 18, 34, 6), True),
            (1343717, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 21, 18, 35, 43),
             True),
            (1343718, 10101, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 21, 18, 35, 49),
             True),
            (1343719, 10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2020, 12, 21, 18, 35, 51),
             True),
            (1347745, 9945, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 8, datetime.datetime(2020, 12, 23, 20, 5, 50), True),
            (1347746, 9947, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 8, datetime.datetime(2020, 12, 23, 20, 6, 22), True),
            (1347752, 9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 8, datetime.datetime(2020, 12, 23, 20, 8, 34), True),
            (1347757, 9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 5, 8, datetime.datetime(2020, 12, 23, 20, 9, 48), True),
            (
            1347765, 9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 8, datetime.datetime(2020, 12, 23, 20, 11, 15), True),
            (1351558, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 18, 52),
             True),
            (1351561, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 19, 50),
             True),
            (
            1351571, 10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 23, 1), True),
            (1351572, 10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 23, 39),
             True),
            (1351575, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 24, 17),
             True),
            (1351576, 10101, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 24, 26),
             True),
            (1351579, 10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 24, 59),
             True),
            (1351583, 10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2020, 12, 28, 18, 25, 49),
             True),
            (1356075, 9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 12, datetime.datetime(2020, 12, 31, 16, 24, 55),
             True),
            (1356142, 9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 12, datetime.datetime(2020, 12, 31, 16, 45, 35),
             True),
            (
            1356192, 9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 12, datetime.datetime(2020, 12, 31, 17, 0, 23), True),
            (1356252, 9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 12, datetime.datetime(2020, 12, 31, 17, 19, 22),
             True),
            (1356254, 9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 12, datetime.datetime(2020, 12, 31, 17, 20, 17),
             True),
            (
            1367020, 11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 1, 13, 11, 42, 2), False),
            (
            1367104, 11032, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 1, 13, 16, 8, 53), False),
            (1368088, 11032, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 16, 14, 18, 22),
             False),
            (1368454, 10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 17, 16, 29, 10),
             False),
            (1368755, 11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 18, 12, 27, 42),
             False),
            (
            1368907, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 1, 18, 16, 42, 30), True),
            (1370392, 11361, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2021, 1, 21, 8, 0, 25), False),
            (1370878, 11359, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 1, 22, 12, 23, 25),
             False),
            (1371054, 10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 22, 17, 44, 49),
             False),
            (
            1371950, 10765, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 23, 17, 7, 18), False),
            (1373087, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 1, 1, datetime.datetime(2021, 1, 25, 2, 13, 45), True),
            (
            1373563, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 25, 18, 57, 1), False),
            (
            1374698, 11032, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 27, 18, 4, 12), False),
            (
            1374809, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 1, 27, 20, 8, 39), False),
            (1375326, 11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2021, 1, 29, 11, 2, 55), True),
            (1375328, 11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2021, 1, 29, 11, 4, 27), True),
            (
            1375483, 11359, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 29, 13, 36, 1), False),
            (
            1376403, 10760, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 1, 30, 6, 24, 22), False),
            (
            1377586, 11359, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 1, 13, 56, 46), False),
            (1377997, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 2, 2, 3, 5, 38), True),
            (1379315, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 4, 15, 58, 7), False),
            (1380216, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 5, 20, 53, 6), False),
            (1380757, 11034, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 2, 6, 16, 0, 35), True),
            (1380758, 11032, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 2, 6, 16, 0, 45), True),
            (
            1380870, 10763, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 6, 17, 46, 43), False),
            (1382132, 10756, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 7, 22, 13, 9), False),
            (1382384, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 8, 2, 48, 53), True),
            (1384458, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 10, 13, 48, 33),
             False),
            (1384980, 10761, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 10, 20, 15, 33),
             False),
            (1385643, 11360, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 11, 11, 27, 35),
             False),
            (1385749, 11360, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 2, 11, 14, 20, 36),
             False),
            (1387599, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 13, 13, 45, 59),
             False),
            (1387793, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 13, 17, 28, 56),
             False),
            (
            1394685, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 19, 9, 13, 17), False),
            (1394739, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 19, 10, 3, 7), False),
            (1395354, 10764, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 2, 20, 1, 47, 4), False),
            (
            1395554, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2021, 2, 20, 14, 59, 57), True),
            (1395555, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 2, 20, 15, 0, 14), True),
            (1395556, 11035, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2021, 2, 20, 15, 0, 18), True),
            (
            1395793, 10758, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2021, 2, 20, 17, 43, 50), True),
            (
            1395795, 10760, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2021, 2, 20, 17, 45, 15), True),
            (
            1395798, 10762, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2021, 2, 20, 17, 47, 44), True),
            (1397282, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 21, 19, 45, 24),
             False),
            (1397789, 10767, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 22, 1, 6, 11), False),
            (
            1400027, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 2, 23, 15, 28, 24), True),
            (1403865, 10758, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 2, 26, 20, 38, 45),
             False),
            (
            1407202, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 1, 14, 37, 16), False),
            (1407227, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 1, 14, 46, 47), True),
            (
            1407292, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 1, 15, 19, 13), False),
            (
            1414108, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 6, 19, 35, 16), False),
            (1414610, 10758, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2021, 3, 7, 2, 29, 57), False),
            (1416295, 11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 8, 10, 22, 5), False),
            (1416365, 11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2021, 3, 8, 11, 9, 17), False),
            (1416473, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 8, 14, 8, 56), True),
            (1418906, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 10, 18, 42, 28),
             False),
            (
            1419389, 11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 11, 12, 8, 43), False),
            (
            1420286, 11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 12, 9, 47, 27), False),
            (
            1424079, 10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2021, 3, 14, 22, 13, 14), True),
            (1424082, 10767, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 14, 22, 13, 55),
             False),
            (
            1424088, 10765, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 6, datetime.datetime(2021, 3, 14, 22, 15, 35), True),
            (1424090, 10766, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 14, 22, 16, 46),
             False),
            (
            1424098, 10760, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2021, 3, 14, 22, 19, 26), True),
            (
            1424104, 10761, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 6, datetime.datetime(2021, 3, 14, 22, 21, 26), True),
            (
            1424860, 10767, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 15, 6, 24, 48), False),
            (
            1425189, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 15, 12, 23, 40), True),
            (1425198, 11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 15, 12, 29, 5), True),
            (
            1425199, 11361, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 15, 12, 29, 33), True),
            (
            1428335, 11363, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 5, 5, datetime.datetime(2021, 3, 17, 12, 11, 34), True),
            (
            1429309, 11361, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 5, datetime.datetime(2021, 3, 18, 10, 58, 33), True),
            (1429310, 11360, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 5, datetime.datetime(2021, 3, 18, 10, 59, 4), True),
            (
            1429311, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 5, datetime.datetime(2021, 3, 18, 10, 59, 34), True),
            (1433105, 11033, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 21, 12, 48, 36),
             False),
            (
            1433128, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 21, 12, 59, 7), False),
            (1433181, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 21, 13, 21, 59),
             False),
            (1433230, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 21, 13, 48, 20),
             False),
            (1433770, 10764, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 21, 18, 16, 18),
             False),
            (
            1433970, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 3, 21, 20, 26, 58), True),
            (1433971, 11034, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 3, 21, 20, 27, 5), True),
            (1434384, 10764, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 22, 1, 42, 8), False),
            (1437629, 11363, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 24, 13, 45, 35),
             False),
            (1437761, 11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 24, 14, 16, 25),
             False),
            (
            1441213, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 3, 26, 13, 17, 29), True),
            (
            1441215, 11033, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2021, 3, 26, 13, 18, 14), True),
            (
            1441222, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 3, datetime.datetime(2021, 3, 26, 13, 21, 43), True),
            (
            1441223, 11035, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 3, datetime.datetime(2021, 3, 26, 13, 21, 56), True),
            (
            1445012, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 3, 28, 14, 33, 45), True),
            (
            1445013, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 28, 14, 33, 59), True),
            (1445521, 10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 3, 28, 19, 15, 13),
             False),
            (1453413, 10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 4, 5, 3, 29, 53), False),
            (1454478, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 4, 6, 3, 16, 1), True),
            (1454705, 11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 4, 6, 12, 9, 17), False),
            (1454737, 11364, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', None, 1, datetime.datetime(2021, 4, 6, 12, 33, 36),
             False),
            (
            1461190, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 4, 11, 14, 5, 32), False),
            (1461211, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 4, 11, 14, 17, 27),
             False),
            (1461289, 11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 4, 11, 15, 13, 19),
             False),
            (1461317, 11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 1, datetime.datetime(2021, 4, 11, 15, 20, 50),
             False),
            (
            1465642, 10762, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2021, 4, 14, 13, 19, 33), True),
            (1465643, 10766, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2021, 4, 14, 13, 21, 4), True),
            (
            1465644, 10765, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 4, datetime.datetime(2021, 4, 14, 13, 27, 13), True),
            (
            1465645, 10758, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 4, datetime.datetime(2021, 4, 14, 13, 29, 43), True),
            (
            1465646, 10760, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 3, 4, datetime.datetime(2021, 4, 14, 13, 30, 40), True),
            (1466348, 11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 4, 1, datetime.datetime(2021, 4, 15, 1, 10, 18), True),
            (
            1466765, 11363, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 2, 1, datetime.datetime(2021, 4, 15, 14, 18, 6), False)]

        gradesample2 = [(9862, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'DataStructures',
                         'Explain and apply data structures to solve a given problem, by providing technical information on the data structure, its abstractions, implementations, and functional operations. Contrast different data structures that support a solution of a given problem.',
                         21, 2486, 'Explain, implement, and apply algorithms and their associated data structures',
                         'CS110',
                         '3.9'), (9863, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'SortingAlgorithms',
                                  'Explain and analyze sorting algorithms whenever needed to adequately solve computational problems.',
                                  21, 2486,
                                  'Explain, implement, and apply algorithms and their associated data structures',
                                  'CS110', '3.5'), (9864, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'RandomizationTechniques',
                                                    'Explain and apply randomization techniques to solve problems and/or augment standard algorithms.',
                                                    21, 2486,
                                                    'Explain, implement, and apply algorithms and their associated data structures',
                                                    'CS110', '3.33333333333333'), (
                            9865, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'DynamicProgramming',
                            'Explain and apply the principles of the dynamic programming algorithmic paradigm. ', 21,
                            2486,
                            'Explain, implement, and apply algorithms and their associated data structures', 'CS110',
                            None), (
                            9866, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'GreedyAlgorithms',
                            'Explain and apply the principles of the greedy algorithmic paradigm. ', 21, 2486,
                            'Explain, implement, and apply algorithms and their associated data structures', 'CS110',
                            '3.0'), (
                            9867, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'ComputationalSolutions',
                            'Demonstrate the ability to formulate algorithmic solutions to computational problems by systematically breaking problems down into a clear, ordered set of concrete steps, and later translate these steps into programming language statements that a computer can execute.',
                            21, 2487,
                            'Determine and apply appropriate algorithms and data structures to solve problems',
                            'CS110', '3.55'), (9868, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'ComputationalCritique',
                                               'Contrast the relative merits of several algorithms or data structures that accomplish the same goal and choose the best option given relevant constraints.',
                                               21, 2487,
                                               'Determine and apply appropriate algorithms and data structures to solve problems',
                                               'CS110', '3.51724137931034'), (
                            9869, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'ComplexityAnalysis',
                            'Analyze the asymptotic behavior of an algorithm or algorithm solution to a problem using the appropriate Big-O, Big-Ω, or Big-Θ notations.',
                            21, 2487,
                            'Determine and apply appropriate algorithms and data structures to solve problems',
                            'CS110', '3.08'), (9870, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'PythonProgramming',
                                               'Write Python programs to implement, analyze, and compare algorithms and apply data structures. Produce Python code to plot and visualize meaningful performance metrics.',
                                               21, 2488,
                                               'Write Python implementation of algorithms and computational applications using best practices for code efficiency and readability',
                                               'CS110', '3.72413793103448'), (
                            9871, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'CodeReadability',
                            'Generate and structure Python code that is clear and concise. Include meaningful comments, choose clear variable names, use naming conventions consistently, and include useful error messages. Strive to produce code that not only works but can also be run by external readers.',
                            21, 2488,
                            'Write Python implementation of algorithms and computational applications using best practices for code efficiency and readability',
                            'CS110', '3.46428571428571'), (10097, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'LinearSystems',
                                                           'Apply the tools of linear systems and interpret the results.',
                                                           21,
                                                           2582,
                                                           '(LinearSystems) Apply the tools of linear systems and interpret the results.',
                                                           'CS111B', '3.625'), (
                            10098, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'Vectors',
                            'Apply the tools of vector spaces and interpret the results.', 21, 2583,
                            '(Vectors) Apply the tools of vector spaces and interpret the results.', 'CS111B', '3.75'),
                        (
                            10099, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'Transformations',
                            'Apply the tools of linear transformations and interpret the results.', 21, 2584,
                            '(Transformations) Apply the tools of linear transformations and interpret the results.',
                            'CS111B',
                            '3.58333333333333'), (10100, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'TheoreticalTools',
                                                  'Employ deductive reasoning or ancillary mathematical techniques to analyze or solve a problem.',
                                                  21, 2585,
                                                  '(MathTools) Apply foundational mathematical tools and interpret the results.',
                                                  'CS111B', '3.51612903225806'), (
                            10101, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'ComputationalTools',
                            'Employ computational tools such as Sage in support to analyze or solve a problem.', 21,
                            2585,
                            '(MathTools) Apply foundational mathematical tools and interpret the results.', 'CS111B',
                            '3.38095238095238'), (10102, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'quantProfessionalism',
                                                  'Apply professional conventions that are appropriate in quantitative fields',
                                                  21, 2586,
                                                  '(MetaMath) Effectively learn and communicate quantitative concepts. Apply professional conventions in quantitate fields.',
                                                  'CS111B', '3.625'),
                        (10103, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'learnQuant',
                         'Apply the science of learning to master quantitative concepts.',
                         21, 2586,
                         '(MetaMath) Effectively learn and communicate quantitative concepts. Apply professional conventions in quantitate fields.',
                         'CS111B', '3.66666666666667'), (
                            9940, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisiondata',
                            'Identify and evaluate opportunities to leverage data (especially big data) and computer-mediated transactions to enable rational decision making.',
                            21, 2515,
                            'Episteme: Students will learn the conceptual frameworks underpinning quantitative methods of causal inference and prediction that are essential for rational evidence-based decision making.',
                            'CS112', '3.76923076923077'),
                        (9941, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisioninference',
                         'Distinguish among problems of descriptive inference, predictive inference, and causal inference, recognizing the circumstances in which these problems overlap, and assessing the utility of these inferential frameworks in realistic settings.',
                         21, 2515,
                         'Episteme: Students will learn the conceptual frameworks underpinning quantitative methods of causal inference and prediction that are essential for rational evidence-based decision making.',
                         'CS112', '4.0'), (
                            9942, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisiontheory',
                            'Explain and critically examine empirical analyses taught in the course, requiring intuitive and mathematical understanding of all key underlying assumptions.',
                            21, 2515,
                            'Episteme: Students will learn the conceptual frameworks underpinning quantitative methods of causal inference and prediction that are essential for rational evidence-based decision making.',
                            'CS112', '3.73333333333333'), (9943, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisionanalysis',
                                                           'Apply empirical methods to decision making.', 21, 2516,
                                                           'Techne: Students will learn to apply computational methods for prediction, classification, and impact estimation, learning the limitations and pitfalls of these methodologies. ',
                                                           'CS112', '3.56'), (
                            9944, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisionreview',
                            'Judge the quality of applied computational methods for decision making.', 21, 2516,
                            'Techne: Students will learn to apply computational methods for prediction, classification, and impact estimation, learning the limitations and pitfalls of these methodologies. ',
                            'CS112', '3.3'), (9945, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisionbrief',
                                              'Effectively present findings and recommendations for statistically sophisticated and less sophisticated audiences (encompassing elements of the HC #professionalism)',
                                              21, 2516,
                                              'Techne: Students will learn to apply computational methods for prediction, classification, and impact estimation, learning the limitations and pitfalls of these methodologies. ',
                                              'CS112', '3.57894736842105'), (
                            9946, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisiondesign',
                            'Decide whether or not (and if so, how) to apply a method to solve a given decision problem, considering real-world factors such as data availability, the standard of evidence required, the anticipated level of effort, likely operationalizability of results.',
                            21, 2517,
                            'Phronesis: Students will learn to assess when and how to apply learnings in realistic decision settings; that is, given a decision problem, how to apply understanding of counterfactual inference and computational methods to inform decision making (i.e., 0',
                            'CS112', '4.36363636363636'), (9947, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'decisionquestion',
                                                           'Frame decision questions in a conceptually coherent and tractable manner.',
                                                           21, 2517,
                                                           'Phronesis: Students will learn to assess when and how to apply learnings in realistic decision settings; that is, given a decision problem, how to apply understanding of counterfactual inference and computational methods to inform decision making (i.e., 0',
                                                           'CS112', '4.0'), (
                            11030, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'differentiation',
                            'Apply the tools of differentiation and interpret the results.', 22, 2844,
                            '(Differentiation) Apply the tools of differentiation and interpret the results.', 'CS111A',
                            '3.9'),
                        (11031, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'integration',
                         'Apply the tools of integration and interpret the results.', 22, 2845,
                         '(Integration) Apply the tools of integration and interpret the results.', 'CS111A',
                         '3.83333333333333'), (11032, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'limitscontinuity',
                                               'Apply the concept of a limit or continuity and interpret the results.',
                                               22,
                                               2846,
                                               '(LimitsContinuity) Apply the concept of a limit or continuity and interpret the results.',
                                               'CS111A', '3.66666666666667'), (
                            11033, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'computationaltools',
                            ' Employ computational tools such as Sage in support to analyze or solve a problem.', 22,
                            2847,
                            '(MathTools) Apply foundational mathematical tools and interpret the results.', 'CS111A',
                            '3.0'), (
                            11034, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'theoreticaltools',
                            'Employ deductive reasoning or ancillary mathematical techniques to analyze or solve a problem.',
                            22, 2847, '(MathTools) Apply foundational mathematical tools and interpret the results.',
                            'CS111A',
                            '4.0'), (11035, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'quantProfessionalism',
                                     'Apply professional conventions that are appropriate in quantitative fields.', 22,
                                     2848,
                                     '(MetaMath) Effectively learn and communicate quantitative concepts. Apply professional conventions in quantitate fields.',
                                     'CS111A', '3.5'), (11036, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'learnQuant',
                                                        'Apply the science of learning to master quantitative concepts.',
                                                        22,
                                                        2848,
                                                        '(MetaMath) Effectively learn and communicate quantitative concepts. Apply professional conventions in quantitate fields.',
                                                        'CS111A', '3.27777777777778'), (
                            10756, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'NeuronsAndMolecules',
                            'Describe events at the level of neurons and molecules, and how they relate to other cogsci levels of analysis',
                            22, 2747,
                            'Describe interactions among different levels of analysis in cognitive science (#cogscilevels)',
                            'SS110', '4.0'), (10757, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'BrainAndMindOrganization',
                                              'Describe events at the level of brain and/or mind organization, and how they relate to other cogsci levels of analysis',
                                              22, 2747,
                                              'Describe interactions among different levels of analysis in cognitive science (#cogscilevels)',
                                              'SS110', None), (
                            10758, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'IndividualPsychology',
                            'Describe events at the level of individual psychology, and how they relate to other cogsci levels of analysis',
                            22, 2747,
                            'Describe interactions among different levels of analysis in cognitive science (#cogscilevels)',
                            'SS110', '3.3'), (10759, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'SocialCognition',
                                              'Describe events at the level of social cognition, and how they relate to other cogsci levels of analysis',
                                              22, 2747,
                                              'Describe interactions among different levels of analysis in cognitive science (#cogscilevels)',
                                              'SS110', '3.7'), (
                            10760, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'ResearcherBestPractices',
                            'Identify and explain how best practices in the field improve research and results', 22,
                            2748,
                            'Design, interpret, and evaluate methods used in cognitive science (#cogscimethods)',
                            'SS110',
                            '3.66666666666667'), (10761, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'SelfReportMeasures',
                                                  'Design, interpret, or evaluate methods that rely on self report', 22,
                                                  2748,
                                                  'Design, interpret, and evaluate methods used in cognitive science (#cogscimethods)',
                                                  'SS110', '4.0'), (
                            10762, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'BehavioralMeasures',
                            'Design, interpret, or evaluate methods that rely on behavioral measures', 22, 2748,
                            'Design, interpret, and evaluate methods used in cognitive science (#cogscimethods)',
                            'SS110',
                            '3.5'), (10763, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'PhysiologicalMeasures',
                                     'Design, interpret, or evaluate methods that rely on physiological measures', 22,
                                     2748,
                                     'Design, interpret, and evaluate methods used in cognitive science (#cogscimethods)',
                                     'SS110', '4.0'),
                        (10764, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'MechanismsOfCognition',
                         'Describe the mechanism of a feature of cognition, and how it relates to other explanation types',
                         22, 2749,
                         'Differentiate between, and describe relations among, distinct explanation types in cognitive science (#cogsciexplanations)',
                         'SS110', '3.33333333333333'), (
                            10765, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'DevelopmentOfCognition',
                            'Describe the development of a feature of cognition, and how it relates to other explanation types',
                            22, 2749,
                            'Differentiate between, and describe relations among, distinct explanation types in cognitive science (#cogsciexplanations)',
                            'SS110', '2.63636363636364'),
                        (10766, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'EvolutionOfCognition',
                         'Describe the evolution of a feature of cognition, and how it relates to other explanation types',
                         22, 2749,
                         'Differentiate between, and describe relations among, distinct explanation types in cognitive science (#cogsciexplanations)',
                         'SS110', '3.0'), (
                            10767, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'FunctionOfCognition',
                            'Describe the function of a feature of cognition, and how it relates to other explanation types',
                            22, 2749,
                            'Differentiate between, and describe relations among, distinct explanation types in cognitive science (#cogsciexplanations)',
                            'SS110', '3.33333333333333'), (11359, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'abstraction',
                                                           ' Design interfaces (class interfaces, user interfaces, etc.) that are easy to use and hide much of the complexity needed for the implementation. ',
                                                           22, 2973,
                                                           'Identify and design the necessary system while keeping it as simple and understandable as possible (#design)',
                                                           'CS162', '3.66666666666667'), (
                            11360, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'separationofconcerns',
                            'Design systems such that any task is handled by exactly one component and each component handles conceptually similar tasks.',
                            22, 2973,
                            'Identify and design the necessary system while keeping it as simple and understandable as possible (#design)',
                            'CS162', '3.14285714285714'), (11361, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'communication',
                                                           'Ensure that all code, documentation and commit messages are clearly written with explanations where appropriate.',
                                                           22, 2974,
                                                           'Collaborate efficiently within a large team through division of labor and standardized practices (#collaboration)',
                                                           'CS162', '3.57142857142857'), (
                            11362, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'agile',
                            'Follow the agile movement when researching and developing a new product. This involves finding short feedback loops throughout all stages of the product lifecycle (inception, development, and deployment).',
                            22, 2974,
                            'Collaborate efficiently within a large team through division of labor and standardized practices (#collaboration)',
                            'CS162', '3.90909090909091'), (11363, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'testing',
                                                           'Write comprehensive and meaningful testing code for the system.',
                                                           22, 2975,
                                                           'Follow industry best practices to minimize introducing bugs and ensuring fast consistent deployment (#reliability)',
                                                           'CS162', '4.28571428571429'), (
                            11364, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'deployment',
                            'Build a deployment process that can quickly scale to many machines if need be.', 22, 2975,
                            'Follow industry best practices to minimize introducing bugs and ensuring fast consistent deployment (#reliability)',
                            'CS162', None), (11365, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'sql',
                                             'Write fast queries for well-designed SQL tables.', 22, 2976,
                                             'Follow best practices for storing and retrieving data (#data)', 'CS162',
                                             '3.6'), (
                            11366, 'gdl2tj4slgrsxy0n6rmd48ehlloys4to', 'webstandards',
                            'Build systems that correctly use the standard web technologies (e.g. http, html)', 22,
                            2977,
                            'Build systems that correctly use the standard web technologies e.g. http, html (#webstandards)',
                            'CS162', '3.3')]

        # add to LoGrade table
        for i in gradesample:
            i = list(i)
            db.session.add(
                LoGrade(grade_id=i[0], lo_id=i[1], user_id=i[2], score=i[3], weight=i[4], time=i[5], assignment=i[6]))

        # add to Lo table
        for i in gradesample2:
            i = list(i)
            db.session.add(
                Lo(lo_id=i[0], user_id=i[1], name=i[2], description=i[3], term=i[4], co_id=i[5], co_desc=i[6],
                   course=i[7],
                   mean=i[8]))

        db.session.commit()

    def test_co_grade_over_time(self):
        # test the function of co_grade_over_time
        result = co_grade_over_time(user_id='gdl2tj4slgrsxy0n6rmd48ehlloys4to', course='CS110')
        self.assertEqual(result.iloc[0][0], '2020-09-08')
        self.assertEqual(result.iloc[-1][1], 3.54)

    def test_co_grade_query(self):
        # test the function of Co_grade_query
        result = Co_grade_query(user_id='gdl2tj4slgrsxy0n6rmd48ehlloys4to')
        df = pd.read_sql(result.statement, db.session.bind)
        self.assertEqual(df[df['course'] == 'CS111A']['cograde'].iloc[0], 3.67)
        self.assertEqual(df[df['course'] == 'CS110']['Letter Grade'].iloc[0], 'A-')
        self.assertEqual(df[df['course'] == 'CS162']['term'].iloc[0], 'Spring 2021')
        self.assertEqual(df[df['course'] == 'SS110']['major'].iloc[0], 'SS')

    def test_calc_course_grade(self):
        # test the function of calc_course_grade
        i = pd.read_sql(
            db.session.query(LoGrade.lo_id, Lo.co_id, Lo.course,
                             (cast(LoGrade.score * LoGrade.weight, Float)).label('grade'),
                             cast(LoGrade.weight, Float), func.DATE(LoGrade.time).label('date')
                             ).filter_by(user_id='gdl2tj4slgrsxy0n6rmd48ehlloys4to').join(Lo,
                                                                                          Lo.lo_id == LoGrade.lo_id).filter(
                Lo.course == 'CS110').order_by(LoGrade.time).statement, db.session.bind)

        self.assertEqual(calc_course_grade(i), 3.54)

    def tearDown(self):
        db.drop_all()
