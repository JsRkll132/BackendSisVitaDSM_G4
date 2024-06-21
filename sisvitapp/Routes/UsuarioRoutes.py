from ..services.Services import diagnosticarService,get_usuarioService, obtener_puntuaciones_form_pacient_Service, obtener_puntuacionesAllService, obtener_respuestasService,obtener_puntuacionesService, InputContentFormService,getUsersService,getUsersService2,userLoginService,userRegisterService,FormQuestionsService,userSubmitFormService,GetAllFormsService
from flask import Blueprint,jsonify,request
from ..models.dbModel import Diagnosticos, Usuarios,Respuestas
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

@users_routes.get('/api/v2/getuserbyid/<int:usuario_id>')
def get_usuarioRoutes(usuario_id)  : 
    try : 
        usuario = get_usuarioService(usuario_id) 
        user_selected = {
            "id": usuario.id,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "correo": usuario.correo,
            "numero_celular": usuario.numero_celular,
            "nombre_usuario": usuario.nombre_usuario,
            "tipo_usuario": usuario.tipo_usuario}
        return jsonify(user_selected)
    except : 
        return jsonify({"status":0,'detail':f'Usuario {usuario_id} no se pudo encontrar.'}),400


@users_routes.post('/api/v2/login')
def userLogin() : 
    try :
        username = request.json['username']
        password = request.json['password']
        userAuth = userLoginService(username=username,password=password)
        print(userAuth[0].id)
        if  userAuth : 
            token = Security.Security().generate_token(userAuth[0])
            print(token)
            return jsonify({'status':'sucess login','token':token,'type_user':userAuth[1]}) , 200
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
        if content['status']==1 :
            return jsonify({'status':content,'sucess':1}),200
        else :
            return content,500
        
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

@users_routes.get('/api/v2/ContentForm/<int:id>')
def  InputContentFormRoutes(id) : 
    try : 
        data = InputContentFormService(id)
        ContentForm = [{'id':point.id,'formulario_id' : point.formulario_id,'respuesta_formulario':point.respuestaformulario,'puntaje':point.puntaje } for point in data]
        return jsonify(ContentForm),200   
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
            return jsonify({'status':db_response,'result_status':1}),200
        else :
            return jsonify({'status':'No es posible añadir','result_status':0}),500
        
    except :
        return jsonify({'status':'ocurrio un error, no se pudo enviar el formulario...','result_status':0}),503


@users_routes.get('/api/v2/obtener/formularioCompletado/paciente/<int:paciente_id>')
def obtener_puntuacionesRoutes(paciente_id) :
    try : 
        formularios_paciente_ = obtener_puntuacionesService(paciente_id)
        formularios_paciente = [{
            'formulario_id':formulario.formulario_id,
            'paciente_id': formulario.paciente_id,
            'usuario_id': formulario.usuario_id,
            'nombres': formulario.nombres,
            'apellido_paterno': formulario.apellido_paterno,
            'apellido_materno': formulario.apellido_materno,
            'tipo_formulario': formulario.tipo_formulario,
            'completado_formulario_id': formulario.completado_formulario_id,
            'fecha_completado':formulario.fecha_completado,
            'suma_puntuacion': formulario.suma_puntuacion
        } for formulario in formularios_paciente_]
        #print(formularios_paciente)
        return jsonify(formularios_paciente)
        
    except : 
        pass

@users_routes.get('/api/v2/obtener/formularioCompletado/all')
def obtener_puntuacionesAllRoutes() :
    try : 
        formularios_paciente_ = obtener_puntuacionesAllService()
        formularios_paciente = [{
            'formulario_id':formulario.formulario_id,
            'paciente_id': formulario.paciente_id,
            'usuario_id': formulario.usuario_id,
            'nombres': formulario.nombres,
            'apellido_paterno': formulario.apellido_paterno,
            'apellido_materno': formulario.apellido_materno,
            'tipo_formulario': formulario.tipo_formulario,
            'completado_formulario_id': formulario.completado_formulario_id,
            'fecha_completado':formulario.fecha_completado,
            'suma_puntuacion': formulario.suma_puntuacion
        } for formulario in formularios_paciente_]
        #print(formularios_paciente)
        return jsonify(formularios_paciente)
        
    except : 
        return None
        pass

@users_routes.get('/api/v2/obtener/respuestas/formularioCompletado/paciente/<int:paciente_id>/formulario_completado/<int:completado_formulario_id>')
def obtener_respuestasRoutes(paciente_id,completado_formulario_id) :
    try : 
        respuesta_formularios_paciente_ = obtener_respuestasService(paciente_id,completado_formulario_id)
        respuesta_formularios_paciente = [{
            'respuesta_id': respuesta.respuesta_id,
            'respuesta': respuesta.respuesta,
            'puntuacion': respuesta.puntuacion,
            'pregunta': respuesta.pregunta
        } for respuesta in respuesta_formularios_paciente_]
        #print(formularios_paciente)
        return jsonify(respuesta_formularios_paciente)
        
    except : 
        pass

@users_routes.get('/api/v2/obtener/formularioCompletado/formulario/<int:completado_formulario_id>')
def obtener_puntuaciones_form_pacient_Routes(completado_formulario_id):
    try:
        formulario_paciente = obtener_puntuaciones_form_pacient_Service(completado_formulario_id)
        if formulario_paciente:
            resultado = {
                'formulario_id':formulario_paciente.formulario_id,
                'paciente_id': formulario_paciente.paciente_id,
                'usuario_id': formulario_paciente.usuario_id,
                'nombres': formulario_paciente.nombres,
                'apellido_paterno': formulario_paciente.apellido_paterno,
                'apellido_materno': formulario_paciente.apellido_materno,
                'tipo_formulario': formulario_paciente.tipo_formulario,
                'completado_formulario_id': formulario_paciente.completado_formulario_id,
                'fecha_completado': formulario_paciente.fecha_completado,
                'suma_puntuacion': formulario_paciente.suma_puntuacion
            }
            return jsonify(resultado),200
        else:
            return jsonify({"error": "No data found"}), 404
    except:
        return jsonify({"error": "An error occurred"}), 500

@users_routes.post('/api/v2/diagnosticar')
def diagnosticarRoute():
    try : 
        data = request.get_json()
        required_fields = ['paciente_id', 'psicologo_id', 'formulario_id', 'completado_formulario_id', 'calificacion', 'diagnostico']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos necesarios','status':0}), 400
        nuevo_diagnostico = Diagnosticos(
            paciente_id=data['paciente_id'],
            psicologo_id=data['psicologo_id'],
            formulario_id=data['formulario_id'],
            completado_formulario_id=data['completado_formulario_id'],
            calificacion=data['calificacion'],
            diagnostico=data['diagnostico']
        )
        sucess = diagnosticarService(nuevo_diagnostico)
        if sucess == None :
            return jsonify({'message': 'Hubo un error a la hora de registrar el diagnostico.','status':-1}), 400
        return jsonify(sucess), 201

    except Exception as e:
         return jsonify({ 'error': str(e)}), 500