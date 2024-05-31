import datetime
from jwt.api_jwt import PyJWT
from dotenv import load_dotenv
import pytz
import os
load_dotenv()
class Security() :
    tz = pytz.timezone('America/Lima')
    @classmethod
    def generate_token(cls,auth_user) :
        payload = {
            'iat' :datetime.datetime.now(tz=cls.tz),
            'exp' :datetime.datetime.now(tz=cls.tz)+datetime.timedelta(minutes=120) ,
            'id_user' : auth_user.id,
            'username' : auth_user.nombre_usuario,          
            'tipo_usuario' : auth_user.tipo_usuario 
             
        }
        print(payload)
        
        print(os.getenv('JWT_KEY'))
        
        key = PyJWT().encode(payload=payload,key=os.getenv('JWT_KEY'),algorithm = 'HS256')
        print (key)
        return PyJWT().encode(payload=payload,key=os.getenv('JWT_KEY'),algorithm = 'HS256')
        
    @classmethod
    def verify_token(cls,headers) : 
        if 'Authorization' in headers.keys() :
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]