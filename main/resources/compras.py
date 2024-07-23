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
        compras = db.session.query(Compramodel).all()
        return jsonify({
            "compras": [compra.to_json() for compra in compras]
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
        compra_exist = Compramodel.from_json(request.get_json())


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

    