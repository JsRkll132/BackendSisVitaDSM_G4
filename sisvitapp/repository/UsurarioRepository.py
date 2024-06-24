from ..models.Usuario import Usuario
from ..models.dbModel import Usuarios
from ..models.dbModel import Pacientes
from ..models.dbModel import Psicologos
from ..models.dbModel import Respuestas
from ..models.dbModel import Preguntas
from ..models.dbModel import CompletadoFormulario
from ..models.dbModel import Formularios
from ..models.dbModel import  ContenidoFormulario
import os 
from sqlalchemy.orm import joinedload
import psycopg2 as pgc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
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
        if user.tipo_usuario == 'paciente' :
            return session.query(Pacientes).filter_by(usuario_id = user.id).first(),0 if (bcrypt.checkpw(password.encode('utf-8'),user.contrasena.encode('utf-8'))) else None
        elif user.tipo_usuario == 'psicologo' : 
            return session.query(Psicologos).filter_by(usuario_id = user.id).first(),1 if (bcrypt.checkpw(password.encode('utf-8'),user.contrasena.encode('utf-8'))) else None
    except : 
        session.rollback()
        return None

def get_usuarioRepository(usuario_id):
    # Consultar la información del usuario
    try : 
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        return usuario
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

    def calculate_level_anxiety(formulario_id,answer_lists) : 
        if formulario_id == 1 : 
            percent_score = 100 * sum([answer.puntuacion for answer in answer_lists])/84
            if percent_score < 25 : 
                return 'NORMAL'
            elif percent_score>=25 and percent_score < 50 : 
                return 'MODERADA'
            elif percent_score>=50 and percent_score < 75 : 
                return 'ALTA'
            else : 
                return 'MUY ALTA'
            
        elif formulario_id == 2 : 
            percent_score = 100 * sum([answer.puntuacion for answer in answer_lists])/80
            if percent_score < 50 : 
                return 'NORMAL'
            elif percent_score>=50 and percent_score < 59 : 
                return 'MODERADA'
            elif percent_score>=60 and percent_score < 69 : 
                return 'ALTA'
            else : 
                return 'MUY ALTA'
        elif formulario_id == 3 : 
            return 'NORMAL'
        else : 
            return 'NORMAL'
        
    try : 
        print('------------')
        level_anxiety = calculate_level_anxiety(answer_lists=answerList,formulario_id=form_id)
        complete_form = CompletadoFormulario(paciente_id=user_id,formulario_id=form_id,nivel_ansiedad = level_anxiety)
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

def InputContentFormRepository(id) :
    try : 
        data = session.query(ContenidoFormulario).filter_by(formulario_id = id).all()
        return data
    except : 
        session.rollback()
        return None

def obtener_puntuaciones_form_pacient_Repository(completado_formulario_id):
    try:
        resultados = session.query(
            Formularios.id.label('formulario_id'),
            Pacientes.id.label('paciente_id'),
            Usuarios.id.label('usuario_id'),
            Usuarios.nombres,
            Usuarios.apellido_paterno,
            Usuarios.apellido_materno,
            Formularios.tipo.label('tipo_formulario'),
            CompletadoFormulario.nivel_ansiedad.label('nivel_ansiedad'),
            CompletadoFormulario.id.label('completado_formulario_id'),
            CompletadoFormulario.fecha_completado.label('fecha_completado'),
            func.sum(Respuestas.puntuacion).label('suma_puntuacion')
        ).join(
            Pacientes, Pacientes.usuario_id == Usuarios.id
        ).join(
            Respuestas, Respuestas.paciente_id == Pacientes.id
        ).join(
            CompletadoFormulario, CompletadoFormulario.id == Respuestas.completado_formulario_id
        ).join(
            Formularios, Formularios.id == CompletadoFormulario.formulario_id
        ).filter(
            CompletadoFormulario.id == completado_formulario_id
        ).group_by(
            Pacientes.id, Usuarios.id,Formularios.id, Formularios.tipo, CompletadoFormulario.id
        ).first()
        return resultados
    except:
        session.rollback()
        return None

def obtener_puntuacionesRepository( paciente_id ):
    try :
            # Realizar la consulta
            # Realizar la consulta
        resultados = session.query(
            Formularios.id.label('formulario_id'),
            Pacientes.id.label('paciente_id'),
            Usuarios.id.label('usuario_id'),
            Usuarios.nombres,
            Usuarios.apellido_paterno,
            Usuarios.apellido_materno,
            Formularios.tipo.label('tipo_formulario'),
            CompletadoFormulario.id.label('completado_formulario_id'),
            CompletadoFormulario.fecha_completado.label('fecha_completado'),
            func.sum(Respuestas.puntuacion).label('suma_puntuacion')
        ).join(
            Pacientes, Pacientes.usuario_id == Usuarios.id
        ).join(
            Respuestas, Respuestas.paciente_id == Pacientes.id
        ).join(
            CompletadoFormulario, CompletadoFormulario.id == Respuestas.completado_formulario_id
        ).join(
            Formularios, Formularios.id == CompletadoFormulario.formulario_id
        ).filter(
            Pacientes.id == paciente_id
        ).group_by(
            Pacientes.id,Usuarios.id,Formularios.id, Formularios.tipo, CompletadoFormulario.id
        ).order_by(
            CompletadoFormulario.id
        ).all()
        #print('-'*50)
        #print(resultados)
        #print('-'*50)
        return resultados
    except : 
        session.rollback()
        return None

def obtener_puntuacionesAllRepository():
    try:
        resultados = session.query(
            Pacientes.id.label('paciente_id'),
            Usuarios.id.label('usuario_id'),
            Usuarios.nombres,
            Usuarios.apellido_paterno,
            Usuarios.apellido_materno,
            Formularios.id.label('formulario_id'),
            Formularios.tipo.label('tipo_formulario'),
            CompletadoFormulario.id.label('completado_formulario_id'),
            CompletadoFormulario.fecha_completado.label('fecha_completado'),
            CompletadoFormulario.nivel_ansiedad.label('nivel_ansiedad'),
            func.sum(Respuestas.puntuacion).label('suma_puntuacion')
        ).join(
            Pacientes, Pacientes.usuario_id == Usuarios.id
        ).join(
            Respuestas, Respuestas.paciente_id == Pacientes.id
        ).join(
            CompletadoFormulario, CompletadoFormulario.id == Respuestas.completado_formulario_id
        ).join(
            Formularios, Formularios.id == CompletadoFormulario.formulario_id
        ).group_by(
            Pacientes.id, Usuarios.id, Formularios.id, Formularios.tipo, CompletadoFormulario.id, CompletadoFormulario.nivel_ansiedad
        ).order_by(
            CompletadoFormulario.id
        ).all()
        return resultados
    except:
        session.rollback()
        return None

def obtener_respuestasRepository(paciente_id,completado_formulario_id ):
    try : 
        respuestas = session.query(
            Respuestas.id.label('respuesta_id'),
            Respuestas.respuesta,
            Respuestas.puntuacion,
            Preguntas.pregunta
        ).join(
            Preguntas, Preguntas.id == Respuestas.pregunta_id
        ).filter(
            Respuestas.paciente_id == paciente_id,
            Respuestas.completado_formulario_id == completado_formulario_id
        ).all()
        return respuestas
    except : 
        session.rollback()
        return  None

def diagnosticarRepository(nuevo_diagnostico) : 
    try : 
        session.add(nuevo_diagnostico)
        session.commit()  
        return {'message': 'Diagnóstico creado exitosamente','status':1}     
    except :
        session.rollback()
        return None
       
