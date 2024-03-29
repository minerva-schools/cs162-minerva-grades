from flask.globals import session
from dashboard import app, db
from dashboard.forms import LoginForm, DropDownList
from dashboard.models import User, Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, cast, case
from sqlalchemy import Float
from dashboard import grade_calculations

import pandas as pd
import os


@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hcs'))

    form = LoginForm()
    if form.validate_on_submit():
        os.environ['SESSION_ID'] = form.sessionID.data

        try:

            user = User(user_id=form.sessionID.data)

            # checks if user is already in database
            if User.query.filter_by(user_id=form.sessionID.data).first() != None:
                login_user(user)
                flash(f'Hi, you have been logged in.', 'success')

                return redirect(url_for('hcs'))

            # if not, add user to db and call forum fetcher
            else:
                db.session.add(user)

                # fetch Hcs
                HcFetch = HcFetcher(form.sessionID.data)
                HcFetch.get_grades()

                # fetch Los
                LoFetch = LoFetcher(form.sessionID.data)
                LoFetch.get_grades()

                db.session.commit()
                login_user(user)

                flash(f'Hi, you have been logged in.', 'success')
                return redirect(url_for('hcs'))
        except:
            flash('Login unsuccessful. Please check Session ID.', 'danger')
            db.session.rollback()

    return render_template('login.html', title='Welcome', form=form)



@app.route("/hcs", methods=['GET', 'POST'])
@login_required
def hcs():
    session_id = os.environ.get("SESSION_ID")
    Course_grades_query = grade_calculations.Hc_grade_query(session_id).all()

    title = "HC Applications"
    headings = ['Name', 'Courses', 'Grade', 'Transferred']

    form = DropDownList()
    available_courses = db.session.query(Hc.course).filter_by(user_id=session_id).distinct().all()
    # form the list of tuples for SelectField
    form.course.choices = [(i, available_courses[i][0]) for i in range(len(available_courses))]
    session['selected_course'] = None

    # get data from the selected field
    if request.method == 'POST':
        course_idx = int(form.course.data)
        course = available_courses[course_idx][0]
        session['selected_course'] = str(course)
        Course_grades_query = grade_calculations.Hc_grade_query(session_id, session['selected_course']).all()
        return render_template('hcs.html', title=title, headings=headings, data=Course_grades_query, form=form,
                               course=course)

    return render_template('hcs.html', title=title, headings=headings, data=Course_grades_query, form=form, course='All Cornerstone Courses')


@app.route("/<hc>")
@login_required
def singleHC(hc):
    os.environ['selected_hc'] = hc
    return render_template('singleHC.html', data=hc)


@app.route("/courses", methods=['GET', 'POST'])
@login_required
def courses():
    session_id = os.environ.get("SESSION_ID")

    form = DropDownList()
    available_courses = db.session.query(Lo.course).filter_by(user_id=session_id).distinct().all()
    # form the list of tuples for SelectField
    form.course.choices = [(i, available_courses[i][0]) for i in range(len(available_courses))]
    session['selected_course'] = None

    # get data from the selected field and render info for the specific course
    if request.method == 'POST':
        course_idx = int(form.course.data)
        course = available_courses[course_idx][0]
        session['selected_course'] = str(course)
        title_course = "LOs grade for " + course
        headings_course = ["LO", "Mean", "Description"]
        LO_grade_by_course = grade_calculations.LO_for_course_grade_query(course).all()
        return render_template('courses.html', title=title_course, headings=headings_course, data=LO_grade_by_course, form=form, course=course, request_method="POST")

    # render for all course info
    title = "Course Info"
    headings = ['Name', 'Major', 'Semester', 'Course Grade', 'Letter Grade']
    Co_grades_query = grade_calculations.Co_grade_query(user_id=session_id).all()
    return render_template('courses.html', title=title, headings=headings, data=Co_grades_query, form=form, course='all', request_method="NONE")

@app.route("/logout")
def logout():
    # empty database for particular user.
    # delete loGrades
    loGrades = LoGrade.query.filter_by(user_id=current_user.get_id()).all()
    for loGrade in loGrades:
        db.session.delete(loGrade)
    # delete hcGrades
    hcGrades = HcGrade.query.filter_by(user_id=current_user.get_id()).all()
    for hcGrade in hcGrades:
        db.session.delete(hcGrade)
    # delete los
    los = Lo.query.filter_by(user_id=current_user.get_id()).all()
    for lo in los:
        db.session.delete(lo)
    # delete hcs
    hcs = Hc.query.filter_by(user_id=current_user.get_id()).all()
    for hc in hcs:
        db.session.delete(hc)

    # delete user after logout
    user = User.query.filter_by(user_id=current_user.get_id()).first()
    #print(user)
    db.session.delete(user)
    db.session.commit()
    logout_user()

    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
