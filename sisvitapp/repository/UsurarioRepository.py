from ..models.Usuario import Usuario
from ..models.dbModel import Ubigeo, Usuarios
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
from sqlalchemy import and_, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from flask import json, jsonify, request
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
def userSubmitFormRepository(answerList,paciente_id,form_id) :

    try : 
        answers_json = json.dumps(answerList)
        session.execute(
            text("""
                CALL submit_form_answers(:paciente_id, :form_id, :answers_json);
                    """),
                {"paciente_id": paciente_id, "form_id": form_id, "answers_json": answers_json}  
            )
        session.commit()
        try : 
            resultados = session.query(
                Formularios.id.label('formulario_id'),
                Pacientes.id.label('paciente_id'),
                Usuarios.id.label('usuario_id'),
                Usuarios.nombres,
                Usuarios.apellido_paterno,
                Usuarios.apellido_materno,
                Usuarios.ubigeo,
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
                Pacientes.id == paciente_id
            ).group_by(
                Pacientes.id, Usuarios.id,Formularios.id, Formularios.tipo, CompletadoFormulario.id
            ).order_by(CompletadoFormulario.id.desc()).first()
            data = {
                    'formulario_id': resultados.formulario_id,
                    'paciente_id': resultados.paciente_id,
                    'usuario_id': resultados.usuario_id,
                    'nombres': resultados.nombres,
                    'apellido_paterno': resultados.apellido_paterno,
                    'apellido_materno': resultados.apellido_materno,
                    'ubigeo': resultados.ubigeo,
                    'tipo_formulario': resultados.tipo_formulario,
                    'nivel_ansiedad': resultados.nivel_ansiedad,
                    'completado_formulario_id': resultados.completado_formulario_id,
                    'fecha_completado': resultados.fecha_completado,
                    'suma_puntuacion': resultados.suma_puntuacion
                }
            print("-------------")
            print(data)
            return data
        except Exception as e : 
            print(str(e))
            session.rollback()
            return None
    except Exception as e : 
        print(str(e))
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
            Usuarios.ubigeo,
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
            Usuarios.ubigeo,
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
            Usuarios.ubigeo,
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
       
def inHeatMapRepository():
    try:
        # Consulta ORM usando SQLAlchemy
        subquery = (
            session.query(
                CompletadoFormulario.paciente_id,
                func.max(CompletadoFormulario.fecha_completado).label("max_fecha_completado")
            )
            .group_by(CompletadoFormulario.paciente_id)
            .subquery()
        )

        query = (
            session.query(
                Usuarios.id.label("id_usuario"),
                Pacientes.id.label("id_paciente"),
                Usuarios.nombres,
                Usuarios.apellido_paterno,
                Usuarios.apellido_materno,
                Usuarios.ubigeo,
                CompletadoFormulario.id.label("id_ultimo_formulario"),
                CompletadoFormulario.nivel_ansiedad,
                CompletadoFormulario.formulario_id.label("id_formulario"),
                Ubigeo.lat.label("latitud"),
                Ubigeo.long.label("longitud")
            )
            .join(Pacientes, Usuarios.id == Pacientes.usuario_id)
            .join(CompletadoFormulario, Pacientes.id == CompletadoFormulario.paciente_id)
            .join(Ubigeo, Usuarios.ubigeo == Ubigeo.ubigeo)
            .join(subquery, and_(
                CompletadoFormulario.paciente_id == subquery.c.paciente_id,
                CompletadoFormulario.fecha_completado == subquery.c.max_fecha_completado
            ))
            .order_by(Usuarios.nombres, Usuarios.apellido_paterno, Usuarios.apellido_materno)
            .all()
        )

        data = [
            {
                'id_usuario': row.id_usuario,
                'id_paciente': row.id_paciente,
                'nombres': row.nombres,
                'apellido_paterno': row.apellido_paterno,
                'apellido_materno': row.apellido_materno,
                'ubigeo': row.ubigeo,
                'latitud': row.latitud,
                'longitud': row.longitud,
                'id_ultimo_formulario': row.id_ultimo_formulario,
                'nivel_ansiedad': row.nivel_ansiedad,
                'id_formulario': row.id_formulario
            }
            for row in query
        ]

        return data
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return None
    
def obtenerDatosUbigeoRepository() :
    try:
        departamentos = session.query(
            Ubigeo.departamento
        ).distinct().order_by(Ubigeo.departamento).all()

        estructura = []
        for departamento in departamentos:
            provincias = session.query(
                Ubigeo.provincia
            ).filter(Ubigeo.departamento == departamento.departamento).distinct().order_by(Ubigeo.provincia).all()

            provincias_estructura = []
            for provincia in provincias:
                distritos = session.query(
                    Ubigeo.distrito,
                    Ubigeo.ubigeo
                ).filter(Ubigeo.provincia == provincia.provincia).order_by(Ubigeo.distrito).all()

                distritos_estructura = [
                    {"distrito": distrito.distrito, "ubigeo": distrito.ubigeo} for distrito in distritos
                ]

                provincias_estructura.append({
                    "provincia": provincia.provincia,
                    "distritos": distritos_estructura
                })

            estructura.append({
                "departamento": departamento.departamento,
                "provincias": provincias_estructura
            })

        return estructura

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return None