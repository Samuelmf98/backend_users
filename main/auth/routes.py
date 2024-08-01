from flask import request, Blueprint
from ..import db
from main.models import Usuariomodel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup

#Creamos un nuevo endpoint
auth = Blueprint("auth", __name__, url_prefix = "/auth")

@auth.route("/login", methods = ["POST"])

def login():
    #Recuperamos los datos que el usuario introduce y los comparamos con los de la tabla usuario para verificar existencia
    usuario = db.session.query(Usuariomodel).filter(Usuariomodel.email == request.get_json().get("email")).first()


    if not usuario:
        return "El email no existe en la base de datos, por favor registrese"
    else:
        #Comprobamos la contraseña con la funcion validate_password del modelo usuario
        if usuario.validate_password(request.get_json().get("contraseña")):

            access_token = create_access_token(identity = usuario)

            data = {
                "id": str(usuario.id),
                "email": usuario.email,
                "token": access_token,
                "role": usuario.role
            }
            return data, 200
        else:

            return "Incorrect Password", 401

@auth.route("/register", methods = ["POST"])

def register():
    usuario = Usuariomodel.from_json(request.get_json())
    print(f"Este es el email introducido: {usuario.email}")

    exists = db.session.query(Usuariomodel).filter(Usuariomodel.email == usuario.email).count() > 0


    if exists:
        return  f"Usuario  con el email {usuario.email} ya registrado", 409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        
    return usuario.to_json(), 201