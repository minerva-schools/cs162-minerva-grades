from dashboard import app, db
from dashboard.models import User, Lo, LoGrade, Hc, HcGrade
from dashboard import grade_calculations
from flask.globals import session

import pandas as pd
import altair as alt
from altair import Chart, X, Y, Axis, Data, DataFormat,Scale

@app.route("/courses/cg")
def course_grade():
    selected_course = session.get('selected_course', None)
    if selected_course == None:
        source = pd.read_sql(grade_calculations.Co_grade_query().statement,db.session.bind)

        # make chart here
        chart = Chart(
            data=source, height=336, width=400).mark_bar().encode(
            Y('cograde:Q',
              scale=Scale(domain=(0, 5))
              ),
            X('course:N'),
            color=alt.Color('course:N', legend=None)).interactive()
        # always return to json.
        return chart.to_json()
    else:
        source = grade_calculations.co_grade_over_time(selected_course)

        # make interactive chart
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['Date'], empty='none')

        # The basic line
        line = alt.Chart(source).mark_line().encode(
            x='Date:N',
            y='Course Grade:Q',
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
            text=alt.condition(nearest, 'Course Grade:Q', alt.value(' '))
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
            width=500, height=336
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
