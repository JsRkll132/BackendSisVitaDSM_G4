from flask import Blueprint, redirect, url_for

import os 
import psycopg2 as pgc

main = Blueprint('main', __name__)
cnn = pgc.connect( os.getenv('DATABASE_URL'))
@main.get('/')
def index():
    return "e_e"

