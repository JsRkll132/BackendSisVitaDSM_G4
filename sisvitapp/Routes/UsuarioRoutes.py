from ..services.Services import getUsersService,getUsersService2,userLoginService,userRegisterService,FormQuestionsService,userSubmitFormService,GetAllFormsService
from flask import Blueprint,jsonify,request
from ..models.dbModel import Usuarios,Respuestas
from ..utils import Security
import bcrypt
import traceback
users_routes = Blueprint('users_routes',__name__)
import jwt
@users_routes.get('/api/v2/getusers')
def getUsersRoute() :
    data =  getUsersService()
    users_list = [ {'id' : int(user.id_usuario),"nombres" : user.nombres,"ap_paterno":user.ap_paterno,
                        "ap_materno":user.ap_materno,
                         'telefono':user.telefono,
                          'dni' : user.dni,
                           'correo':user.correo[0],
                           'tipo_usuario':user.tipo_usuario } for user in data]
    return jsonify(users_list)


@users_routes.get('/api/v2/getusers2')
def getUsersRoute2() : 
    data = getUsersService2()
    users_list = [{'id':user.id,'apellido_paterno' : user.apellido_paterno,'apellido_materno':user.apellido_materno
                   ,'contrasena':user.contrasena,'correo':user.correo,'nombre_usuario':user.nombre_usuario,'nombres':user.nombres
                   ,'numero_celular':user.numero_celular,'tipo_usuario':user.tipo_usuario} for user in data]
    return jsonify(users_list)


@users_routes.post('/api/v2/login')
def userLogin() : 
    try :
        username = request.json['username']
        password = request.json['password']
        userAuth = userLoginService(username=username,password=password)
        print(userAuth.id)
        if  userAuth : 
            token = Security.Security().generate_token(userAuth)
            print(token)
            return jsonify({'status':'sucess login','token':token}) , 200
        else :
            return jsonify({'status':'icorrect login'}) ,401
    except Exception as e:
        errorstack = str(traceback.format_exc())
        return jsonify({"Error":str(e),"traceback_error":errorstack})
    
@users_routes.post('/api/v2/register')   
def userRegister() : 
    try :
        nombre_usuario = request.json['nombre_usuario']
        nombres = request.json['nombres']
        apellido_paterno = request.json['apellido_paterno']
        apellido_materno = request.json['apellido_materno']
        contrasena = bcrypt.hashpw(request.json['contrasena'].encode('utf-8'), bcrypt.gensalt()) 
        correo = request.json['correo']
        tipo_usuario = request.json['tipo_usuario']
        numero_celular = request.json['numero_celular']
        
        new_user = Usuarios(nombre_usuario = nombre_usuario,nombres = nombres,
                            apellido_paterno = apellido_paterno,apellido_materno = apellido_materno,
                            contrasena = contrasena.decode('utf-8'),
                            correo = correo,
                            tipo_usuario = tipo_usuario,
                            numero_celular = numero_celular
                            )
        content = userRegisterService(new_user)
        if content :
            return jsonify({'status':content}),200
        else :
            return jsonify({'status':'No es posible añadir'}),500
        
    except :
        return jsonify({'status':'ocurrio un error...'}),503


@users_routes.get('/api/v2/questions/<int:id>')
def FormQuestionsRoutes(id) : 
    try : 
        data = FormQuestionsService(id)
        questions = [{'id':user.id,'formulario_id' : user.formulario_id,'pregunta':user.pregunta} for user in data]
        return jsonify(questions),200
    
    except :
        return jsonify({"status":"Ocurrio un error en la solicitud"}),500

@users_routes.get('/api/v2/forms')
def GetAllFormsRoutes() : 
    try : 
        data = GetAllFormsService()
        questions = [{'id':form_.id,'formulario_tipo' : form_.tipo,'Descripcion':form_.descripcion} for form_ in data]
        return jsonify(questions),200
    
    except :
        return jsonify({"status":"Ocurrio un error en la solicitud"}),500
    

@users_routes.post('/api/v2/llenarFormulario')   
def userSubmitFormRoutes() : 
    try :
        paciente_id = request.json['paciente_id']
        formulario_id = request.json['formulario_id']
        respuestas = [Respuestas(respuesta = rpta['respuesta'],
                                 puntuacion =rpta['puntuacion'],pregunta_id = rpta['pregunta_id'],paciente_id = rpta['paciente_id']) for rpta in  request.json['respuestas']] 
        for resp in respuestas :
            print(resp.puntuacion)
        db_response = userSubmitFormService(answerList=respuestas,user_id=paciente_id,form_id=formulario_id)
        if db_response :
            return jsonify({'status':db_response}),200
        else :
            return jsonify({'status':'No es posible añadir'}),500
        
    except :
        return jsonify({'status':'ocurrio un error, no se pudo enviar el formulario...'}),503
