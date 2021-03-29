from flask.globals import session
from dashboard import app
from dashboard.forms import LoginForm
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))
    form = LoginForm()      
    if form.validate_on_submit():
      user = Lo.query.filter_by(user_id =form.sessionID.data).first()
      if user:
          login_user(user)
          flash(f'Hi {user.user_id}, you have been logged in.', 'success')
          return redirect(url_for('dashboard'))
    return render_template('login.html', title='Welcome', form=form)


@app.route("/dashboard")
def dashboard():
    #posts = Post.query.all()
    return render_template('dashboard.html')#,posts= posts)