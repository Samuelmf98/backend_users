from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import Usuariomodel
from main.auth.decorators import role_required
class Clientes(Resource):
    
    #Se le añade la opcion para comprobar si el usuario que realiza la peticion es admin o no
    #Luego intentamos realizar un get de todos los clientes y nos dira que no podemos. Para activarlo tenemos que logearnos con un usuario admin, coger el JWT y
    #cuando intentemos obetener de nuevo los clientes pegamos antes el JWT en la opcion Auth dentro del postman
    @role_required(roles = ["admin"])
    def get(self):
        clientes = db.session.query(Usuariomodel).filter(Usuariomodel.role == "cliente")
        for cliente in clientes:
            print(cliente)
        page = 1
        per_page = 5
        if request.content_type == 'application/json':
            json_data = request.get_json()
            if json_data:
                for key, value in json_data.items():
                    if key == "page":
                        page = int(value)
                    elif key == "per_page":
                        per_page = int(value)
        clientes = clientes.paginate(page, per_page, True, 10)

        return jsonify({
        "clientes": [cliente.to_json() for cliente in clientes.items],
        "total": clientes.total,
        "pages": clientes.pages,
        "page": page
        })


    def post(self):
        clientes = Usuariomodel.from_json(request.get_json())

        db.session.add(clientes)
        db.session.commit()
        return clientes.to_json(), 201


class Cliente(Resource):
    pass