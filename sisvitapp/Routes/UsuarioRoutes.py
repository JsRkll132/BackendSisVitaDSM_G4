from ..services.Services import getUsersService
from flask import Blueprint,jsonify,request


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



