from ..services.Services import getUsersService,getUsersService2,userLoginService,userRegisterService
from flask import Blueprint,jsonify,request
from ..models.dbModel import Usuarios
import bcrypt
users_routes = Blueprint('users_routes',__name__)

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
        if userLoginService(username=username,password=password) : 
            return jsonify({'status':'sucess login'}) , 200
        else :
            return jsonify({'status':'icorrect login'}) ,401
    except :
        return jsonify({'error':'missing arguments'}) , 503
    
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
