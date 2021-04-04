from GradeFetcher import GradeFetcher, HcFetcher, LoFetcher
from sqlalchemy.orm import sessionmaker  
import sqlalchemy
from sqlalchemy import func, asc
from __init__ import db

def calculate_co_score(co_id):
    '''
    Input: Course outcome ID
    Output: Course outcome score, based on weighted average of all LO grade that belongs to this Course outcome
    '''
    #Get all the score and weight of LO grade with the input co_id
    #SELECT * FROM LoGrade 
    # JOIN Lo
    # ON LoGrade.lo_id = Lo.lo_id
    # WHERE LO.co_id = co_id;
    Lo_grades_query = db.session.query(
        LoGrade.score, LoGrade.weight
        ).join(Lo, LoGrade.c.lo_id == Lo.c.lo_id
        ).filter_by(Lo.co_id == co_id).all()

    total = 0
    sum_weight = 0

    for grade in Lo_grades_query:
        total += grade.score * grade.weight
        sum_weight += grade.weight
    co_score = total/sum_weight
    return co_score

def calculate_course_score(course_code):
    '''
    Input: course string
    Output: course score, based on weighted average of all LO grade belonging to the course
    '''
    #Get all the score and weight of LO grade with the input course code
    Lo_grades_query = db.session.query(
        LoGrade.score, LoGrade.weight
        ).join(Lo, LoGrade.c.lo_id == Lo.c.lo_id
        ).filter_by(Lo.course == course_code).all()
    
    total = 0
    sum_weight = 0

    for grade in Lo_grades_query:
        total += grade.score * grade.weight
        sum_weight += grade.weight
    
    course_score = total / sum_weight

    return course_score

def calculate_gpa():
    '''
    Calculate GPA by take average of all course score
    '''
    courses = db.session.query(Lo.course).distinct() #get all the courses name currently having grades
    total = 0
    course_count  = 0
    for course in courses:
        total += calculate_course_score(course)
        course_count += 1
    gpa = total / course_count
    return gpa

def least_Lo():
    '''
    Return lo_id of the least frequently applied LO, measured by frequency in LoGrade table
    '''
    least_lo = db.session.query(LoGrade.lo_id,         
        func.count(LoGrade.lo_id).label('qty')
        ).group_by(LoGrade.lo_id
        ).order_by(asc('qty')).first()
    return least_lo

    return least_lo

def least_Hc():
    '''
    Return hc_id of the least frequently applied HC, measured by frequency in HcGrade table
    '''
    least_hc = db.session.query(HcGrade.hc_id),
        func.count(HcGrade.hc_id).label('qty')
        ).group_by(HcGrade.hc_id
        ).order_by(asc('qty')).first()
    return least_hc

