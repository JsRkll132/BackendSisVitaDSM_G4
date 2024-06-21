from ..repository.UsurarioRepository import diagnosticarRepository, get_usuarioRepository, obtener_puntuaciones_form_pacient_Repository, obtener_puntuacionesAllRepository,obtener_respuestasRepository,obtener_puntuacionesRepository,InputContentFormRepository,getUsers,userLoginRepository,userRegisterRepostory,FormQuestionsRepository,userSubmitFormRepository,GetAllFormsRepository
from ..models.dbModel import Usuarios
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, CheckConstraint, Index
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
import os
from flask import request
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

def getUsersService() :
    return getUsers()

def getUsersService2() : 
    return session.query(Usuarios).all()

def userLoginService(username,password) :

    return userLoginRepository(username,password)

def userRegisterService(user) :
    return userRegisterRepostory(user=user)

def FormQuestionsService(id):
    return FormQuestionsRepository(id)

def userSubmitFormService(answerList,user_id,form_id) :
    return  userSubmitFormRepository(answerList,user_id,form_id)
def GetAllFormsService() :
    return GetAllFormsRepository() 

def InputContentFormService(id) : 
    return InputContentFormRepository(id)

def obtener_puntuacionesService(paciente_id) : 
    return obtener_puntuacionesRepository(paciente_id)

def obtener_respuestasService(paciente_id,completado_formulario_id):
    return obtener_respuestasRepository(paciente_id,completado_formulario_id)

def get_usuarioService(usuario_id) : 
    return get_usuarioRepository(usuario_id)

def  diagnosticarService(nuevo_diagnostico) : 
    return  diagnosticarRepository(nuevo_diagnostico)


def obtener_puntuacionesAllService() : 
    return obtener_puntuacionesAllRepository()

def obtener_puntuaciones_form_pacient_Service(completado_formulario_id):
    return obtener_puntuaciones_form_pacient_Repository(completado_formulario_id)