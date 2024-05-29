from flask import Blueprint, redirect, url_for,request,jsonify

import os 
import psycopg2 as pgc
from .models.Usuario import Usuario
GET_USERS = 'SELECT * FROM usuario'

main = Blueprint('main', __name__)
cnn = pgc.connect( os.getenv('DATABASE_URL'))
@main.get('/')
def index():
    return "e_e"

@main.get('/api/getusers')
def getUsers() :
    with cnn.cursor() as cursor :
        cursor.execute(GET_USERS) 
        data = cursor.fetchall()
        
        users = [Usuario(id_usuario=user[0],nombres=user[4],ap_paterno=user[5],ap_materno=user[6],telefono=  user[7],dni=user[8],correo=user[9],tipo_usuario=user[10]) for user in data ] 
                        
        users_list = [ {'id' : int(user.id_usuario),"nombres" : user.nombres,"ap_paterno":user.ap_paterno,
                        "ap_materno":user.ap_materno,
                         'telefono':user.telefono,
                          'dni' : user.dni,
                           'correo':user.correo[0],
                           'tipo_usuario':user.tipo_usuario } for user in users ] 
        return jsonify(users_list)
                       
        return users