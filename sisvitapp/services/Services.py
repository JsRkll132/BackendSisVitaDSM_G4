from ..repository.UsurarioRepository import getUsers,userLoginRepository,userRegisterRepostory,FormQuestionsRepository,userSubmitFormRepository,GetAllFormsRepository
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