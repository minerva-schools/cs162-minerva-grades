from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker  
from sqlalchemy import create_engine 

engine = create_engine('sqlite:///:memory:', echo = True)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'de26a2ccabac416b0cc068d4051cee04'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#start session
Session = sessionmaker(bind=engine)
session = Session() 

from dashboard import routes
