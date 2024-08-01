from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import ProductoCompramodel, Compramodel, Productomodel

class ProductosCompras(Resource):
    def post(self):
        prodcompras = ProductoCompramodel.from_json(request.get_json())

        #Comprobar que compraId y productoId existe en las tablas productos y compras
        compras_exist = db.session.query(Compramodel).filter(Compramodel.id == prodcompras.compraId).first()
        productos_exist = db.session.query(Productomodel).filter(Productomodel.id == prodcompras.productoId).first()

        if compras_exist and productos_exist:

            db.session.add(prodcompras)
            db.session.commit()
            return prodcompras.to_json(), 201
        
        elif not compras_exist and not productos_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prodcompras.productoId} no existe en la tabla productos y el id {prodcompras.compraId} no existe en la tabla compras"}))

        elif not compras_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prodcompras.compraId} no existe en la tabla compras" }))
        
        elif not productos_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prodcompras.productoId} no existe en la tabla productos"}))
    
    def get(self):
        page = 1
        per_page = 5
        prodcompras = db.session.query(ProductoCompramodel)
        if request.content_type == 'application/json':
            json_data = request.get_json()
            if json_data:
                for key, value in json_data.items():
                    if key == "page":
                        page = int(value)
                    elif key == "per_page":
                        per_page = int(value)

        prodcompras = prodcompras.paginate(page, per_page, True, 15)
        return jsonify({
            "prodcompras": [prodcompra.to_json() for prodcompra in prodcompras.items],
            "total": prodcompras.total,
            "pages": prodcompras.pages,
            "page": page
            })

class ProductoCompra(Resource):
    def delete(self, id):
        prodcompras = db.session.query(ProductoCompramodel).get_or_404(id)
        db.session.delete(prodcompras)
        db.session.commit()
        return prodcompras.to_json()
    

    def put(self, id):
        prodcompras = db.session.query(ProductoCompramodel).get_or_404(id)

        prod_compras_exist = ProductoCompramodel.from_json(request.get_json()) #Este es el json que le pasas en postman
        compras_exist = db.session.query(Compramodel).filter(Compramodel.id == prod_compras_exist.compraId).first()
        productos_exist = db.session.query(Productomodel).filter(Productomodel.id == prod_compras_exist.productoId).first()

        if compras_exist and productos_exist:

            data = request.get_json().items()
            for clave, valor in data:
                setattr(prodcompras, clave, valor)

            db.session.add(prodcompras)
            db.session.commit()
            return make_response(jsonify({"success": f"Se ha modificado correctamente el registro con el id {prodcompras.id}"}))
        
        elif not compras_exist and not productos_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prod_compras_exist.productoId} no existe en la tabla productos y el id {prod_compras_exist.compraId} no existe en la tabla compras"}))

        elif not compras_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prod_compras_exist.compraId} no existe en la tabla compras" }))
        
        elif not productos_exist:
            return make_response(jsonify({"error": f"Error al insertar datos porque el id {prod_compras_exist.productoId} no existe en la tabla productos"}))

