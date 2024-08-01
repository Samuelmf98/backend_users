from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(roles):
    def decorator(funcion):
        def wrapper(*args, **kwargs):
            verify_jwt_in_request() #verificar que el jwt es correcto   
            claims = get_jwt() #Obtenemos las peticiones que estan dentro del jwt
            if claims["sub"]["role"] in roles: #La clave es sub y dentro accedemos al valor de role
                return funcion(*args, **kwargs)
            else:
                return "Rol  no permitido"

        return wrapper
    
    return decorator

#Estos decoradores vienen dentro de jwt pero los redefinimos

@jwt.user_identity_loader #Esto viene dentro de jwt directamente, luego se importa a routes pero no se usa directamente sino indirectamente cuando se llama a create_access_token
def user_identity_lookup(usuario):
    return {
        "usuarioId": usuario.id,
        "role": usuario.role
    }


#Este no lo usamos para el registro y el login. Lo usamos para
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        "id": usuario.id,
        "role": usuario.role,
        "email": usuario.email
    }
