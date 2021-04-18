from flask.globals import session
from dashboard import app, db
from dashboard.forms import LoginForm
from dashboard.models import User,Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, cast, case
from sqlalchemy import Float

import pandas as pd
from altair import Chart, X, Y, Axis, Data, DataFormat,Scale


@app.route("/", methods=['GET', 'POST'])
@app.route("/login",methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))

    form = LoginForm()      
    if form.validate_on_submit():

        try:  
            
            user = User(user_id=form.sessionID.data)

            print(user)
            #checks if user is already in database
            if User.query.filter_by(user_id = form.sessionID.data).first() != None:
                login_user(user)
                flash(f'Hi, you have been logged in.', 'success')
                print("old user")

                return redirect(url_for('dashboard'))

            #if not, add user to db and call forum fetcher
            else:
                db.session.add(user)  

                #fetch Hcs
                HcFetch = HcFetcher(form.sessionID.data)
                HcFetch.get_grades()

                #fetch Los
                LoFetch = LoFetcher(form.sessionID.data)
                LoFetch.get_grades()

                db.session.commit()
                login_user(user)
                print("new user")


                flash(f'Hi, you have been logged in.', 'success')
                return redirect(url_for('dashboard'))
        except:
            flash('Login unsuccessful. Please check Session ID.', 'danger')
            db.session.rollback()



    return render_template('login.html', title='Welcome', form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/hcs")
@login_required
def hcs():
    return render_template('hcs.html')


@app.route("/courses")
@login_required
def courses():
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
        Lo_grades_query.c.course).all()

    title = "Dataviz course"
    headings = ['Name', 'Major', 'Semester', 'Cograde']

    return render_template('courses.html', title=title, headings=headings, data=Co_grades_query)


@app.route("/settings")
@login_required
def settings():
    return render_template('settings.html')


@app.route("/logout")
def logout():
    #empty database for particular user.
    #delete loGrades
    loGrades = LoGrade.query.filter_by(user_id = current_user.get_id()).all()
    for loGrade in loGrades:
        db.session.delete(loGrade)
    #delete hcGrades
    hcGrades = HcGrade.query.filter_by(user_id = current_user.get_id()).all()
    for hcGrade in hcGrades:
        db.session.delete(hcGrade)
    #delete los
    los = Lo.query.filter_by(user_id = current_user.get_id()).all()
    for lo in los:
        db.session.delete(lo)
    #delete hcs
    hcs = Hc.query.filter_by(user_id = current_user.get_id()).all()
    for hc in hcs:
        db.session.delete(hc)

    #delete user after logout
    user = User.query.filter_by(user_id = current_user.get_id()).first()
    print(user)
    db.session.delete(user)
    db.session.commit()
    logout_user()

    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
