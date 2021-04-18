from dashboard import app, db
from dashboard.models import User, Lo, LoGrade, Hc, HcGrade
from dashboard import grade_calculations

import pandas as pd
import altair as alt
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

@app.route("/courses/cg")
def course_grade():
    # query data
    source = grade_calculations.co_grade_over_time('CS110')

    # make interactive chart
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Date'], empty='none')

    # The basic line
    line = alt.Chart(source).mark_line().encode(
        x='Date:N',
        y='Co_grade:Q',
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='Date:N',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'Co_grade:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='Date:N',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )

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
