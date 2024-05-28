from dbinstance import db




class usuario(db.Model) : 
    id_usuario = db.Column(db.Integer,primary_key = True)