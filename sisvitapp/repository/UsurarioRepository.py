from ..models.Usuario import Usuario
from ..models.dbModel import Usuarios
from ..models.dbModel import Pacientes
from ..models.dbModel import Psicologos
from ..models.dbModel import Respuestas
from ..models.dbModel import Preguntas
import os 
import psycopg2 as pgc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import request
import bcrypt

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

def getUsers() : 
    cnn = pgc.connect(os.getenv('DATABASE_URL'))
    with cnn.cursor() as cursor : 
        cursor.execute('SELECT*FROM usuarios')
        data = cursor.fetchall()
        cursor.close()
        users =  [Usuario(id_usuario=user[0],nombres=user[4],ap_paterno=user[5],ap_materno=user[6],telefono=  user[7],dni=user[8],correo=user[9],tipo_usuario=user[10]) for user in data ]
        return users 
    
def userLoginRepository(username , password) :
    
    user = session.query(Usuarios).filter_by(nombre_usuario = username).first()
    return user if bcrypt.checkpw(password.encode('utf-8'),user.contrasena.encode('utf-8')) else None


def userRegisterRepostory(user) :
    try : 
        session.add(user)
        # Confirmar la transacción
        session.commit()
        if user.tipo_usuario == 'paciente':
            paciente = Pacientes(usuario_id=user.id)
            session.add(paciente)
        elif user.tipo_usuario == 'psicologo':
            psicologo = Psicologos(usuario_id=user.id)
            session.add(psicologo)
        session.commit()
        return f'User  : \"{user.nombre_usuario}\" has been created succesfully.'
    except : 
        return None
    
def beckQuestionsRepository() :
    try : 
        data = session.query(Preguntas).filter_by(formulario_id=1).all()
        return data
    except : 
        return None