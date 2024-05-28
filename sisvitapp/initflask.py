
from flask import Flask
from dotenv import load_dotenv
from .routes import main
import os
import psycopg2
#load_dotenv()

load_dotenv()

def create_app() : 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL')
    app.register_blueprint(main)

    return app


