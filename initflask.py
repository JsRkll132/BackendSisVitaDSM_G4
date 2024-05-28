from dbinstance import db
from flask import Flask
import os

def create_app() : 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://jsrkll132:C5rlOPDIITGyytFNjFvCtMZyteO0k6kR@dpg-cpagk1lds78s73d1tc9g-a/sisvita_db_g4'
    db.init_app(app)