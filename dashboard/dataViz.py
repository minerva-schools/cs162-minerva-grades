from dashboard import app, db
from dashboard.models import User, Lo, LoGrade, Hc, HcGrade

import pandas as pd
from altair import Chart, X, Y, Axis, Data, DataFormat,Scale

#data routing url, referenced by parse in templates
@app.route("/courses/lo")
def Lo_demo():
    #query data here
    LoData = pd.read_sql(db.session.query(Lo).statement,db.session.bind)

    #make chart here
    chart = Chart(
        data=LoData, height=400, width=400).mark_bar().encode(
            Y('mean:Q', 
            scale=Scale(domain=(0, 5))
            ),
            X('course:N'), 
            color='course:N').interactive()
    #always return to json.
    return chart.to_json()
    
@app.route("/hcs/hc")
def Hc_demo():
    HcData = pd.read_sql(db.session.query(Hc).statement,db.session.bind)

    chart = Chart(
    data=HcData, height=400, width=800).mark_bar().encode(
        Y('mean:Q', 
        scale=Scale(domain=(0, 5))
        ),
        X('name:N'), 
        color='course:N').interactive()

    return chart.to_json()