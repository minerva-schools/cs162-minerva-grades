from dashboard.GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from dashboard import db
from dashboard.models import Hc, HcGrade, LoGrade, Lo
import pandas as pd
from sqlalchemy import cast, Float, func, case


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

def Co_grade_query():
    # query Lo grades
    Lo_grades_query = db.session.query(
        Lo.course, Lo.co_id, Lo.term,
        (cast(func.sum(LoGrade.score * LoGrade.weight), Float) / cast(func.sum(LoGrade.weight), Float)).label("cograde")
    ).join(Lo, Lo.lo_id == LoGrade.lo_id).group_by(Lo.co_id).subquery("Lo_grades_query")

    # query co grades and add major information
    Co_grades_query = db.session.query(Lo_grades_query.c.course,
                                       case([(Lo_grades_query.c.course.like('CS%'), 'Computational Science'),
                                             (Lo_grades_query.c.course.like('SS%'), 'Social Science'),
                                             (Lo_grades_query.c.course.like('AH%'), 'Arts & Humanities'),
                                             (Lo_grades_query.c.course.like('NS%'), 'Natural Science')
                                             ], else_='Business').label('major'),
                                       Lo_grades_query.c.term,
                                       func.round((func.avg(Lo_grades_query.c.cograde)), 2).label('cograde')).group_by(
        Lo_grades_query.c.course)

    print(Co_grades_query)

    return Co_grades_query

def LO_for_course_grade_query(course):
    LO_for_course = db.session.query(Lo.name, Lo.mean, Lo.description).filter(Lo.course==course)
    print(LO_for_course)

    return LO_for_course
