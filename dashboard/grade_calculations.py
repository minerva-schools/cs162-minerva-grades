from dashboard.GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from dashboard import db
from dashboard.models import Hc, HcGrade, Lo
import pandas as pd
import math


def get_transfers(user_id, course, end_date=None):
    """For a certain course and timeframe, gives a dataframe with the HCs for that course,
     augmented with their transfer information, including transfer weight, transfer score, and 0 or 1 depending on
     whether or not the HC was transferred"""
    if end_date:
        hcs = pd.read_sql(db.session.query(Hc).filter_by(user_id=user_id).filter_by(course=course).statement,
                          db.session.bind)
        grades = pd.read_sql(db.session.query(HcGrade).filter_by(user_id=user_id).filter(HcGrade.time <= course)
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
    """Calculates the Minerva score (1-5) for a cornerstone at a certain time, including transfers"""
    hcs = get_transfers(user_id, course, time)
    mastery = hcs["mean"].mean()
    transfer_competence = hcs["transfer_score"].mean()
    transferred_percent = hcs["transferred"].mean()
    transfer_scope = min(1 + 2.35 * (transferred_percent / 0.4), 5)
    print(mastery, transfer_competence, transfer_scope)
    score = 0.6 * mastery + 0.25 * transfer_scope + 0.15 * transfer_competence
    return round(score, 2)
