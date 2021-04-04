from flask.globals import session
from dashboard import app, db
from dashboard.forms import LoginForm
from dashboard.models import User,Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import GradeFetcher, LoFetcher, HcFetcher
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))


    form = LoginForm()      
    if form.validate_on_submit():

        user = User(user_id=form.sessionID.data)
        db.session.add(user)
        db.session.commit()

        fetcher = LoFetcher(form.sessionID.data)
        fetcher.get_grades()

        user_fetched = Lo.query.filter_by(user_id = form.sessionID.data).first()

        if user and user_fetched:
            login_user(user)
            flash(f'Hi {user.user_id}, you have been logged in.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

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
    form = LoginForm()      
    return render_template('login.html', title='Welcome', form=form)