from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import Usuariomodel

class Usuarios(Resource):
    
    def post(self):
        usuarios = Usuariomodel.from_json(request.get_json())
        db.session.add(usuarios)
        db.session.commit()
        return usuarios.to_json(), 201
    
    def get(self):
        page = 1
        per_page = 5
        usuarios = db.session.query(Usuariomodel)
        if request.content_type == 'application/json':
            json_data =  request.get_json()
            if json_data:
                for key, value in json_data.items():
                    if  key == "page":
                        page = int(value)
                    elif key == "per_page":
                        per_page = int(value)
        usuarios = usuarios.paginate(page, per_page, True, 15)

        return jsonify({
            "usuarios": [usuario.to_json() for usuario in usuarios.items],
            "total": usuarios.total,
            "pages": usuarios.pages,
            "page": page
            
        })

class Usuario(Resource):
    def get(self, id):
        try:
            usuario = db.session.query(Usuariomodel).get_or_404(id)
            return jsonify(
                {"usuario": usuario.to_json()}
            )
        except:
            return make_response(jsonify({"error": f"Error al obtener usuario con id {id}"}))

    def delete(self, id):
        usuario = db.session.query(Usuariomodel).get_or_404(id)

        try:
            db.session.delete(usuario)
            db.session.commit()
            return make_response(jsonify({"success": f"El usuario con id {id} ha sido eliminado"}))
    
        except:
            return make_response(jsonify({"error": f"Error al eliminar el usuario con id {id}"}))

    def put(self, id):
        usuario = db.session.query(Usuariomodel).get_or_404(id)
        data = request.get_json().items()

        try:
            for clave, valor in data:
                setattr(usuario, clave, valor)

            db.session.add(usuario)
            db.session.commit()
            return make_response(jsonify({"success": f"El usuario con id {id} ha sido modificado"}))
        except:
            return make_response(jsonify({"error": f"Error al modificar el usuario con id {id}"}))