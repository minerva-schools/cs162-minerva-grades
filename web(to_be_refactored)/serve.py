from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Lo(db.Model):
    __tablename__ = "los"
    __table_args__ = {'extend_existing': True}  # Makes sure database is updated and we don't get errors on restart

    lo_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))  # Short LO name. Example: #linearsystems
    description = db.Column(db.String(500))  # Longer LO description
    term = db.Column(db.Integer)  # Integer indicating the term. For example, 22 means Spring 2021
    co_id = db.Column(db.Integer)  # ID of associated Course Outcome
    co_desc = db.Column(db.String(500))  # Description of associated Course Outcome
    course = db.Column(db.String(10))  # Short Course name. Example: CS162
    mean = db.Column(db.String(4))  # Mean of HC score
    # mean would ideally be a numeric but sqlite does not support numerics

class LoGrade(db.Model):
    __tablename__ = "lo_grades"

    grade_id = db.Column(db.Integer, primary_key=True)
    lo_id = db.Column(db.Integer, db.ForeignKey(Lo.lo_id))
    user_id = db.Column(db.Integer, db.ForeignKey(Lo.user_id))
    score = db.Column(db.Integer)  # Score (1-5)
    weight = db.Column(db.Integer)  # Score Weight
    time = db.Column(db.DateTime)  # Date and time the score was received
    assignment = db.Column(db.Boolean)  # Whether the score was received for an assignment

    __table_args__ = (db.ForeignKeyConstraint([lo_id, user_id],
                                              [Lo.lo_id, Lo.user_id]),
                      {'extend_existing': True})
    lo = db.relationship("Lo", foreign_keys=[lo_id, user_id], back_populates="grades")


Lo.grades = db.relationship("LoGrade", foreign_keys=[LoGrade.lo_id, LoGrade.user_id], back_populates="lo")


class Hc(db.Model):
    __tablename__ = "hcs"
    __table_args__ = {'extend_existing': True}

    hc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))  # Short HC name. Example: #powerdynamics
    description = db.Column(db.String(500))  # Longer HC description
    course = db.Column(db.String(10))  # Short Course name. Example: EA
    mean = db.Column(db.String(4))  # Mean of HC score.
    # mean would ideally be a numeric but sqlite does not support numerics


class HcGrade(db.Model):
    __tablename__ = "hc_grades"

    grade_id = db.Column(db.Integer, primary_key=True)
    hc_id = db.Column(db.Integer, db.ForeignKey('hcs.hc_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('hcs.user_id'))
    score = db.Column(db.Integer)  # Score (1-5)
    weight = db.Column(db.Integer)  # Score Weight
    time = db.Column(db.DateTime)  # Date and time the grade was received
    assignment = db.Column(db.Boolean)  # Whether the grade was received for an assignment
    transfer = db.Column(db.Boolean)  # Whether the grade counts for transfer

    __table_args__ = (db.ForeignKeyConstraint([hc_id, user_id],
                                              [Hc.hc_id, Hc.user_id]),
                      {'extend_existing': True})
    hc = db.relationship("Hc", foreign_keys=[hc_id, user_id], back_populates="grades")


Hc.grades = db.relationship("HcGrade", foreign_keys=[HcGrade.hc_id, HcGrade.user_id], back_populates="hc")


db.create_all()
example_grade = Lo(lo_id=1, user_id=1, name="#test", description="test stuff", term=22, co_id=1,
                   co_desc="hello", course="test", mean=3)  # Make sure to delete before moving to production
db.session.merge(example_grade)
db.session.commit()





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run()
