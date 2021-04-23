from dashboard import app, db
from dashboard.models import User, Lo, LoGrade, Hc, HcGrade
from dashboard import grade_calculations
from flask.globals import session
from flask import redirect
from datetime import datetime

import pandas as pd
import os
import altair as alt
from altair import Chart, X, Y, Axis, Data, DataFormat, Scale
from functools import reduce

@app.route("/courses/cg")
def course_grade():
    session_id = os.environ.get("SESSION_ID")
    selected_course = session.get('selected_course', None)
    # show all course grades if haven't selected course from dropdown
    if selected_course == None:
        source = pd.read_sql(grade_calculations.Co_grade_query(session_id).statement, db.session.bind)

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
        # show individual course trend for the selected course from dropdown list
        source = grade_calculations.co_grade_over_time(session_id, selected_course)

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


@app.route("/hcs/hcgrade")
def hc_grade():
    session_id = os.environ.get("SESSION_ID")
    selected_course = session.get('selected_course', None)
    # show all course grades if haven't selected course from dropdown
    if selected_course == None:
        HcData = pd.read_sql(db.session.query(Hc).filter_by(user_id=session_id).statement, db.session.bind)
        final = Chart(
            data=HcData, height=300, width=450).mark_bar().encode(
            Y('mean:Q',
              axis=alt.Axis(title='HC Forum Score'),
              scale=Scale(domain=(0, 5))
              ),
            X('name:N', axis=alt.Axis(title=None),),
            color='course:N').interactive()
    else:
        # query data
        df = grade_calculations.hc_grade_over_time(session_id, selected_course)

        longdata = df.melt('Date', var_name='course', value_name='grade')
        data = longdata[longdata['grade'].notnull()]

        def getBaseChart():
            """
              Creates a chart by encoding the Data along the X positional axis and rolling mean along the Y positional axis
            """

            base = (
                alt.Chart(data)
                    .encode(
                    x=alt.X(
                        "Date:T",
                        axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=0),
                    ),
                    y=alt.Y(
                        "grade:Q",
                        axis=alt.Axis(title=None),
                        scale=Scale(domain=(0, 5))
                    ),
                    color=alt.Color('course:N', legend=None)
                ).properties(width=400, height=336)
            )

            return base

        def getSelection():
            """
              This function creates a selection element and uses it to conditionally set a color for a categorical variable (course).
              It return both the single selection as well as the Category for Color choice set based on selection.
            """
            radio_select = alt.selection_multi(
                fields=["course"], name="Course",
            )

            course_color_condition = alt.condition(
                radio_select, alt.Color("course:N", legend=None), alt.value("lightgrey")
            )

            return radio_select, course_color_condition

        def createChart():
            """
              This function uses the "base" encoding chart to create a line chart.
              The highlight_course variable uses the mark_line function to create a line chart out of the encoding.
              The color of the line is set using the conditional color set for the categorical variable using the selection.
              The chart is bound to the selection using add_selection.
              It also creates a selector element of a vertical array of circles so that the user can select between courses.
            """

            radio_select, course_color_condition = getSelection()

            make_selector = (
                alt.Chart(data)
                    .mark_circle(size=220)
                    .encode(
                    y=alt.Y("course:N", title="Click on circle"),
                    color=course_color_condition
                ).add_selection(radio_select)
            )

            base = getBaseChart()

            highlight_course = (
                base.mark_line(strokeWidth=2)
                    .add_selection(radio_select)
                    .encode(color=course_color_condition,
                            opacity=alt.condition(radio_select, alt.value(1.0), alt.value(0.2)))
            ).properties(title="Rolling Weighted Average of Cornerstone Courses")

            return base, make_selector, highlight_course, radio_select

        def createTooltip(base, radio_select):
            """
              This function uses the "base" encoding chart and the selection captured.
              Four elements related to selection are created here
            """
            # Create a selection that chooses the nearest point & selects based on x-value
            nearest = alt.selection(
                type="single", nearest=True, on="mouseover", fields=["Date"], empty="none"
            )

            # Transparent selectors across the chart. This is what tells us
            # the x-value of the cursor
            selectors = (
                alt.Chart(data)
                    .mark_point()
                    .encode(
                    x="Date:T",
                    opacity=alt.value(0),
                ).add_selection(nearest)
            )

            # Draw points on the line, and highlight based on selection
            points = base.mark_point().encode(
                color=alt.Color("course:N", legend=None),
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
            ).transform_filter(radio_select)

            # Draw text labels near the points, and highlight based on selection
            tooltip_text = base.mark_text(
                align="left",
                dx=5,
                dy=-5,
                fontSize=12
                # fontWeight="bold"
            ).encode(
                text=alt.condition(
                    nearest,
                    alt.Text("grade:Q", format=".2f"),
                    alt.value(" "),
                ),
            ).transform_filter(radio_select)

            # Draw a rule at the location of the selection
            rules = (
                alt.Chart(data)
                    .mark_rule(color="black", strokeWidth=1)
                    .encode(
                    x="Date:T",
                ).transform_filter(nearest)
            )

            return selectors, rules, points, tooltip_text

        base, make_selector, highlight_course, radio_select = createChart()
        selectors, rules, points, tooltip_text = createTooltip(base, radio_select)
        # Bring all the layers together with layering and concatenation
        final = (make_selector | alt.layer(highlight_course, selectors, points, rules, tooltip_text))
    return final.to_json()


@app.route("/singleHC/<hc>")
def single_hc_grade(hc):
    session_id = os.environ.get("SESSION_ID")
    # query data
    source = grade_calculations.single_hc_wavg(session_id, hc)

    data = source[['Date', 'Forum Grade', 'Transfer Grade']]
    df = data.melt('Date', var_name='Transfer', value_name='Grade')
    df['weight'] = list(source['Weight'].values) + list(source['Transfer Weight'].values)

    line = alt.Chart(df, height=400, width=800).mark_line().encode(
        alt.X('Date:T', axis=alt.Axis(title=None, format=("%Y-%m-%d"), labelAngle=0)),
        alt.Y('Grade:Q', title=None), color='Transfer:N').properties(width=900, height=360)

    points = line.mark_point(filled=True).encode(
        alt.X('Date:T', axis=alt.Axis(title=None, format=("%Y-%m-%d"), labelAngle=0)),
        alt.Y('Grade:Q', scale=alt.Scale(domain=(0, 5))),
        size=alt.Size('weight', title='Weight'))

    text = line.mark_text(align='center', baseline='bottom', dy=-7).encode(text=alt.Text("Grade:Q", format=".2f"))

    chart = alt.layer(line, points, text)

    return chart.to_json()