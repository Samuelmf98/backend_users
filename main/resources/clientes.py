from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import Usuariomodel

class Clientes(Resource):
    
    def get(self):
        clientes = db.session.query(Usuariomodel).filter(Usuariomodel.role == "cliente")
        page = 1
        per_page = 5
    
        json_data = request.get_json()
        if json_data:
            for key, value in json_data.items():
                if key == "page":
                    page = int(value)
                elif key == "per_page":
                    per_page = int(value)

        clientes = clientes.paginate(page, per_page, True, 10)

        return jsonify({
        "clientes": [cliente.to_json() for cliente in clientes .items],
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