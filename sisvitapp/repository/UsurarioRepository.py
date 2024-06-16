from ..models.Usuario import Usuario
from ..models.dbModel import Usuarios
from ..models.dbModel import Pacientes
from ..models.dbModel import Psicologos
from ..models.dbModel import Respuestas
from ..models.dbModel import Preguntas
from ..models.dbModel import CompletadoFormulario
from ..models.dbModel import Formularios
from ..models.dbModel import RespuestaFormulario
from ..models.dbModel import  PuntajesFormulario
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
    try :
        user = session.query(Usuarios).filter_by(nombre_usuario = username).first()
        return user if bcrypt.checkpw(password.encode('utf-8'),user.contrasena.encode('utf-8')) else None
    except : 
        session.rollback()
        return None


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
        return {'User': f'\"{user.nombre_usuario}\" has been created succesfully.','status':1}
    except Exception as e : 
        session.rollback()
        return {'error_sis':e,'status':0}
    
def FormQuestionsRepository(id_) :
    try : 
        data = session.query(Preguntas).filter_by(formulario_id=id_).all()
        return data
    except : 
        session.rollback()
        return None
def GetAllFormsRepository() : 
    try : 
        data = session.query(Formularios).all()
        return data
    except : 
        session.rollback()
        return None
def userSubmitFormRepository(answerList,user_id,form_id) :
    try : 
        print('------------')
        complete_form = CompletadoFormulario(paciente_id=user_id,formulario_id=form_id)
        try : 
            session.add(complete_form)
            session.commit()
            cform_id = complete_form.id
            [session.add(Respuestas(respuesta = answer.respuesta,puntuacion = answer.puntuacion,pregunta_id = answer.pregunta_id
                                    ,paciente_id = answer.paciente_id,completado_formulario_id=cform_id)) for answer in answerList ]
            session.commit()
            return f'Response has been submited succesfully.'
        except Exception as e:
            session.rollback()
            print(str(e)) 

    except  : 
        session.rollback()
        return None

def AnswerFormQuestionsRepository(id) :
    try : 
        data = session.query(RespuestaFormulario).filter_by(formulario_id = id).all()
        return data
        
    except : 
        session.rollback()
        return None
    
def PointFormQuestionsRepository(id) :
    try : 
        data = session.query(PuntajesFormulario).filter_by(formulario_id = id).all()
        return data
        
    except : 
        session.rollback()
        return None
    
