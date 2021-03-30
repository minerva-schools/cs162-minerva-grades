from flask.globals import session
from dashboard import app
from dashboard.forms import LoginForm
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard.GradeFetcher import GradeFetcher, LoFetcher, HcFetcher
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
   # if current_user.is_authenticated:
   #   return redirect(url_for('dashboard'))
    form = LoginForm()      
    if form.validate_on_submit():
      fetcher = LoFetcher(form.sessionID.data)
      fetcher.get_grades()

      user = Lo.query.filter_by(user_id =form.sessionID.data).first()
      if user:
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