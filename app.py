import psycopg2
from flask import Flask
import os

app = Flask(__name__)

@app.get('/')
def home() : 
    return 'hello world'