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
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))

    form = LoginForm()      
    if form.validate_on_submit():

        try:
            db.create_all()

            user = User(user_id=form.sessionID.data)

          #  if user != User.query.filter_by(user_id=form.sessionID.data).first():
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
            flash('Login Unsuccessful. Please Check Session ID', 'danger')

        else:
            #checks if fetcher request went through
            if user and userHcFetched and userLoFetched:
                login_user(user)
                flash(f'Hi, you have been logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check session ID', 'danger')
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

@app.route("/singleCourse")
@login_required
def singleCourse():
    return render_template('singlecourse.html')

@app.route("/logout")
def logout():
    logout_user()
    db.drop_all() #wipes data on logout
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
