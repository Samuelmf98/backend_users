from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import Compramodel, Usuariomodel

class Compras(Resource):
    def post(self):
        compras = Compramodel.from_json(request.get_json())

        #Comprobar que el id_usuario de compras existe en usuario
        usuario_exist = db.session.query(Usuariomodel).filter(Usuariomodel.id == compras.usuarioId).first()

        if usuario_exist:
            db.session.add(compras)
            db.session.commit()
            return compras.to_json(), 201
        else:
            return make_response(jsonify({"error:": f"No se puede añadir la compra porque el usuario {compras.usuarioId} no existe"}))

    def get(self):
        page = 1
        per_page = 5
        compras = db.session.query(Compramodel)
        if request.content_type == 'application/json':
            json_data =  request.get_json()
            if json_data:
                for key, value in json_data.items():
                    if key == "page":
                        page = int(value)
                    elif key == "per_page":
                        per_page = int(value)
        compras = compras.paginate(page, per_page, True, 15)


        return jsonify({
            "compras": [compra.to_json() for compra in compras.items],
            "total": compras.total,
            "pages": compras.pages,
            "page": page
        })
    
class Compra(Resource):
    def get(self, id):
        compra = db.session.query(Compramodel).get_or_404(id)
        return compra.to_json()
    
    def delete(self, id):
        compra = db.session.query(Compramodel).get_or_404(id)
        try:
            db.session.delete(compra)
            db.session.commit()
            return make_response(jsonify({"success": f"Compra con id {id} eliminada"}), 404)
        except:
            return make_response(jsonify({"error": f"Error al elimninar la compra con id {id}"}, 404))
        
    def put(self, id):  
        compra = db.session.query(Compramodel).get_or_404(id)
        print(f"Esta es la compra {compra}")

        #Comprobar que el id_usuario de compras existe en usuario
        compra_exist = Compramodel.from_json(request.get_json()) #Este es el json que le pasas en postman


        usuario_exist = db.session.query(Usuariomodel).filter(Usuariomodel.id == compra_exist.usuarioId).first()

        if usuario_exist:

            data = request.get_json().items()
            for clave, valor in data:
                setattr(compra, clave, valor)

            try:
                db.session.add(compra)
                db.session.commit()
                return make_response(jsonify({"success": f"La compra con id {id} ha sido modificada"}))
            except:
                return make_response(jsonify({"error": f"Error al modificar la compra con id {id}"}))
            
        else:
            return make_response(jsonify({"error:": f"No se puede añadir la compra porque el usuario {compra_exist.usuarioId} no existe"}))

    