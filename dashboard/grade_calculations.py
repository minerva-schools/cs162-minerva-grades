from dashboard.GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from dashboard import db
from dashboard.models import Hc, HcGrade
import pandas as pd

def get_transfers():
    hcs = pd.read_sql(db.session.query(Hc).statement, db.session.bind)
    grades = pd.read_sql(db.session.query(HcGrade).statement, db.session.bind)
    for hc in hcs:
        grades 
