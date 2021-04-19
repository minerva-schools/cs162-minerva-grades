from dashboard.GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from dashboard import db
from dashboard.models import Hc, HcGrade, LoGrade, Lo
import pandas as pd
from sqlalchemy import cast, Float, func


def get_transfers():
    hcs = pd.read_sql(db.session.query(Hc).statement, db.session.bind)
    grades = pd.read_sql(db.session.query(HcGrade).statement, db.session.bind)
    for hc in hcs:
        grades


def calc_course_grade(i):
    """
    This function calculates co_grade
    Input:
    - Dataframe includes column of weighted grade and weight

    Output:
    the course_grade
    """
    group_by_grade = i.groupby(by=['co_id'])['grade'].sum()
    group_by_weight = i.groupby(by=['co_id'])['weight'].sum()
    co_grade = group_by_grade / group_by_weight
    return round(co_grade.mean(),2)


def co_grade_over_time(course):
    """
    This function calculates co_grade over time for a selected course
    Input:
    course name
    Output:
    - Dataframe with columns of dates and the respective co_grade
    """
    i = pd.read_sql(
        db.session.query(LoGrade.lo_id, Lo.co_id, Lo.course,
                         (cast(LoGrade.score * LoGrade.weight, Float)).label('grade'),
                         cast(LoGrade.weight, Float), func.DATE(LoGrade.time).label('date')).join(Lo,
                                                                                                  Lo.lo_id == LoGrade.lo_id).filter(
            Lo.course == course).order_by(LoGrade.time).statement, db.session.bind)

    dates = i['date'].unique()
    result = []
    for date in dates:
        current = i.loc[i['date'] <= date]
        co_grade = calc_course_grade(current)
        result.append([date, co_grade])

    df = pd.DataFrame(result, columns=['Date', 'Course Grade'])

    return df
