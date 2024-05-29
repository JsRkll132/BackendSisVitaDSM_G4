from ..models.Usuario import Usuario
import os 
import psycopg2 as pgc


def getUsers() : 
    cnn = pgc.connect(os.getenv('DATABASE_URL'))
    with cnn.cursor() as cursor : 
        cursor.execute('SELECT*FROM usuario')
        data = cursor.fetchall()
        cursor.close()
        users =  [Usuario(id_usuario=user[0],nombres=user[4],ap_paterno=user[5],ap_materno=user[6],telefono=  user[7],dni=user[8],correo=user[9],tipo_usuario=user[10]) for user in data ]
        return users 