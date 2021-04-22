from dashboard.GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from dashboard import db
from dashboard.models import Hc, HcGrade, Lo, LoGrade
import pandas as pd
import math
from sqlalchemy import cast, Float, func, case


def get_transfers(user_id, course, end_date=None):
    """For a certain course and timeframe, gives a dataframe with the HCs for that course,
     augmented with their transfer information, including transfer weight, transfer score, and 0 or 1 depending on
     whether or not the HC was transferred"""
    if end_date:
        hcs = pd.read_sql(db.session.query(Hc).filter_by(user_id=user_id).filter_by(course=course).statement,
                          db.session.bind)
        grades = pd.read_sql(db.session.query(HcGrade).filter_by(user_id=user_id).filter(HcGrade.time <= end_date)
                             .statement, db.session.bind)
    else:
        hcs = pd.read_sql(db.session.query(Hc).filter_by(user_id=user_id).filter_by(course=course).statement,
                      db.session.bind)
        grades = pd.read_sql(db.session.query(HcGrade).filter_by(user_id=user_id).statement, db.session.bind)
    # I haven't been able to nail the exact calculation here, but this should do a decent enough job at it
    courses_taken = 9 + db.session.query(Lo.course).distinct().count()
    hcs["transfer_weight"] = 0
    hcs["transfer_score"] = float(0)
    hcs["transferred"] = 0
    hcs["mean"] = hcs["mean"].astype(float)
    for hc in hcs.itertuples():
        transfer_grades = grades.query('hc_id == {} & transfer'.format(hc.hc_id))
        transfer_weight = transfer_grades[transfer_grades.score >= 3].weight.sum() - \
                          transfer_grades[transfer_grades.score < 3].weight.sum()
        transfer_score = calc_transfer(transfer_weight, courses_taken)
        hcs.at[hc.Index, "transfer_weight"] = transfer_weight
        hcs.at[hc.Index, "transfer_score"] = transfer_score
        hcs.at[hc.Index, "transferred"] = 1 if transfer_score >= 3 else 0
    return hcs


def calc_transfer(weight, courses_taken):
    """Calculates the transfer score for an HC """
    # a bunch of constants that Minerva uses
    alpha = 0.385
    mu = 0.2
    v = 1.818
    return 1 + (4 / (1 + math.e ** (-alpha * (weight - (mu * courses_taken)))) ** v)


def calc_cornerstone_score(user_id, course, time):
    """
    Calculates the Minerva score (1-5) for a cornerstone at a certain time, including transfers.
    This function is appropriate for calculating the grade before a specific time.
    """
    hcs = get_transfers(user_id, course, time)
    mastery = hcs["mean"].mean()
    transfer_competence = hcs["transfer_score"].mean()
    transferred_percent = hcs["transferred"].mean()
    transfer_scope = min(1 + 2.35 * (transferred_percent / 0.4), 5)
    #print(mastery, transfer_competence, transfer_scope)
    score = 0.6 * mastery + 0.25 * transfer_scope + 0.15 * transfer_competence
    return round(score, 2)


def calc_cornerstone_score_timeseries(hcs):
    """
    Calculates the Minerva score (1-5) for a cornerstone at a certain time, including transfers
    This function is suitable for calculating the cornerstone grades based on time series data.
    Input:
    - Dataframe

    Output:
    the course_grade
    """
    mastery = hcs["mean"].mean()
    transfer_competence = hcs["transfer_score"].mean()
    transferred_percent = hcs["transferred"].mean()
    transfer_scope = min(1 + 2.35 * (transferred_percent / 0.4), 5)
    score = 0.6 * mastery + 0.25 * transfer_scope + 0.15 * transfer_competence
    return round(score, 2)


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
    return round(co_grade.mean(), 2)


def co_grade_over_time(user_id, course):
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
                         cast(LoGrade.weight, Float), func.DATE(LoGrade.time).label('date')
                         ).filter_by(user_id=user_id).join(Lo, Lo.lo_id == LoGrade.lo_id).filter(
            Lo.course == course).order_by(LoGrade.time).statement, db.session.bind)

    dates = i['date'].unique()
    result = []
    for date in dates:
        current = i.loc[i['date'] <= date]
        co_grade = calc_course_grade(current)
        result.append([date, co_grade])

    df = pd.DataFrame(result, columns=['Date', 'Course Grade'])
    return df

  
def Co_grade_query(user_id):
    # query Lo grades
    Lo_grades_query = db.session.query(
        Lo.course, Lo.co_id, Lo.term,
        (cast(func.sum(LoGrade.score * LoGrade.weight), Float) / cast(func.sum(LoGrade.weight), Float)).label("cograde")
    ).filter_by(user_id=user_id).join(Lo, Lo.lo_id == LoGrade.lo_id).group_by(Lo.co_id).subquery("Lo_grades_query")

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


def calc_hc_grade(i):
    """
    This function calculates hc_grade
    Input:
    - Dataframe includes column of weighted grade and weight

    Output:
    the hc_grade
    """
    group_by_grade = i.groupby(by=['hc_id'])['grade'].sum()
    group_by_weight = i.groupby(by=['hc_id'])['weight'].sum()
    hc_grade = group_by_grade / group_by_weight
    return round(hc_grade.mean(), 2)


def calc_single_hc_grade(i):
    """
    This function calculates the single hc_grade
    Input:
    - Dataframe includes column of weighted grade and weight

    Output:
    the hc_grade
    """
    group_by_grade = i['grade'].sum()
    group_by_weight = i['weight'].sum()
    hc_grade = group_by_grade / group_by_weight
    return round(hc_grade.mean(), 2)


def hc_grade_over_time(user_id, Courses):
    """
    This function calculates cornerstone course's grade over time for a selected course
    Input:
    - Course name, e.g. 'FA'

    Output:
    - Dataframe with columns of dates and the respective hc_grade
    """
    i = pd.read_sql(
        db.session.query(HcGrade.hc_id, Hc.hc_id, Hc.course, HcGrade.transfer, Hc.mean, HcGrade.score,
                         (cast(HcGrade.score * HcGrade.weight, Float)).label('grade'),
                         cast(HcGrade.weight, Float), func.DATE(HcGrade.time).label('date')
                         ).filter_by(user_id=user_id).join(Hc, Hc.hc_id == HcGrade.hc_id).filter(
            Hc.course == Courses).order_by(HcGrade.time).statement, db.session.bind)

    courses_taken = 9 + db.session.query(Lo.course).distinct().count()
    i["transfer_weight"] = 0
    i["transfer_score"] = float(0)
    i["transferred"] = 0
    i["mean"] = i["mean"].astype(float)
    for hc in i.itertuples():
        transfer_grades = i.query('hc_id == {} & transfer'.format(hc.hc_id))
        transfer_weight = transfer_grades[transfer_grades.score >= 3].weight.sum() - \
                          transfer_grades[transfer_grades.score < 3].weight.sum()
        transfer_score = calc_transfer(transfer_weight, courses_taken)
        i.at[hc.Index, "transfer_weight"] = transfer_weight
        i.at[hc.Index, "transfer_score"] = transfer_score
        i.at[hc.Index, "transferred"] = 1 if transfer_score >= 3 else 0

    dates = i['date'].unique()
    result = []
    for date in dates:
        current = i.loc[i['date'] <= date]
        hc_grade = calc_hc_grade(current)
        transfer_grade = calc_cornerstone_score_timeseries(current)
        result.append([date, hc_grade, transfer_grade])

    df = pd.DataFrame(result, columns=['Date', '{0}'.format(Courses), '{0} Transfer'.format(Courses)])
    df.to_csv('transfer.csv')
    return df

def calc_gpa(grade):
    """Calculates GPA for a course based on its score
    Input:
    - A minerva course score (1-5)

    Output:
    - A tuple with the GPA score (e.g. 3.7 for A-) and letter grade (e.g. B+)
    """
    conversion = {4: (4, "A+"), 3.55: (4, "A"), 3.35: (3.7, "A-"), 3.15: (3.3, "B+"), 2.95: (3, "B"), 2.75: (2.7, "B-"),
                  2.6: (2.3, "C+"), 2.5: (2, "C"), 2.25: (1.7, "C-"), 2: (1.3, "D"), 1: (1, "F")}
    for threshold, letter_grade in conversion.items():
        if grade >= threshold:
            return letter_grade
    raise ValueError("Grade is smaller than 1")

def single_hc_wavg(user_id, HcName):
    """
    This function calculates the single HC's rolling weighted average.
    Input:
    - HC name, e.g.'interpretivelens'

    Output:
    - Dataframe with all the relevant info contrasting transfer & non-transfer
    """
    i = pd.read_sql(
        db.session.query(HcGrade.hc_id, Hc.hc_id, Hc.course, HcGrade.transfer, Hc.mean, HcGrade.score,
                         (cast(HcGrade.score * HcGrade.weight, Float)).label('grade'),
                         cast(HcGrade.weight, Float), func.DATE(HcGrade.time).label('date')
                         ).filter_by(user_id=user_id).join(Hc, Hc.hc_id == HcGrade.hc_id).filter(
            Hc.name == HcName).order_by(HcGrade.time).statement, db.session.bind)

    courses_taken = 9 + db.session.query(Lo.course).distinct().count()
    i["transfer_weight"] = 0
    i["transfer_score"] = float(0)
    i["transferred"] = 0
    i["mean"] = i["mean"].astype(float)
    for hc in i.itertuples():
        transfer_grades = i.query('hc_id == {} & transfer'.format(hc.hc_id))
        transfer_weight = transfer_grades[transfer_grades.score >= 3].weight.sum() - \
                          transfer_grades[transfer_grades.score < 3].weight.sum()
        transfer_score = calc_transfer(transfer_weight, courses_taken)
        i.at[hc.Index, "transfer_weight"] = transfer_weight
        i.at[hc.Index, "transfer_score"] = transfer_score
        i.at[hc.Index, "transferred"] = 1 if transfer_score >= 3 else 0

    dates = i['date'].unique()
    result = []
    for date in dates:
        current = i.loc[i['date'] <= date]
        current_weight = i.loc[i.date == date, 'weight'].values[0]
        hc_grade = calc_single_hc_grade(current)
        hc_transfer = i.loc[i.date == date, 'transfer_score'].values[0]
        hc_transfer_weight = i.loc[i.date == date, 'transfer_weight'].values[0]
        result.append([date, current_weight, HcName, hc_grade, hc_transfer, hc_transfer_weight])

    df = pd.DataFrame(result, columns=['Date', 'Weight', 'HCName', 'Forum Grade', 'Transfer Grade', 'Transfer Weight'])

    return df