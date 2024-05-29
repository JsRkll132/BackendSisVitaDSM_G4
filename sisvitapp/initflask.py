
from flask import Flask
from dotenv import load_dotenv
from .routes import main
from .Routes.UsuarioRoutes import users_routes
import os
import psycopg2
#load_dotenv()

load_dotenv()

def create_app() : 
    app = Flask(__name__)
    print('SS')
    app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL')
    app.register_blueprint(main)
    app.register_blueprint(users_routes)
    return app


