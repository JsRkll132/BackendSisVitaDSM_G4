from dbinstance import db
from flask import Flask
#from dotenv import load_dotenv
import os
#load_dotenv()
def create_app() : 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://jsrkll132:GRyZwb4RJJxzcTkU8STWWsaXIlejldHo@dpg-cpb3sqvjbltc73esea30-a.oregon-postgres.render.com/dsm_241_g4"
    db.init_app(app)


create_app()