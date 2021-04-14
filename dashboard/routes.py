from flask.globals import session
from dashboard import app, db
from dashboard.forms import LoginForm
from dashboard.models import User,Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import LoFetcher, HcFetcher
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

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
            db.session.add(user)
            db.session.commit()

            #fetch HCs
            HcFetch = HcFetcher(form.sessionID.data)
            HcFetch.get_grades()
            userHcFetched = Hc.query.filter_by(user_id = form.sessionID.data).first()

            #fetch Los
            LoFetch = LoFetcher(form.sessionID.data)
            LoFetch.get_grades()
            userLoFetched = Lo.query.filter_by(user_id = form.sessionID.data).first()

        except:
            flash('Login unsuccessful. Please check Session ID.', 'danger')

        else:
            #checks if fetcher request went through
            if user and userHcFetched and userLoFetched:
                login_user(user)
                flash(f'Hi, you have been logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check Session ID.', 'danger')
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
    return render_template('courses.html')


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
    db.session.delete(user)
    db.session.commit()
    logout_user()

    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
