from flask_restful import Resource
from flask import request, jsonify, make_response
from .. import db
from main.models import Productomodel

class Productos(Resource):
    def post(self):
        producto = Productomodel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201
    
    def get(self):
        page = 1
        per_page = 5 #Cuantos elementos por pagina
        productos = db.session.query(Productomodel)

        json_data = request.get_json()
        if json_data:
            for key, value in json_data.items():
                if key == "page":
                    page = int(value)
                elif key == "per_page":
                    per_page = int(value)

        productos = productos.paginate(page, per_page, True, 15)

        return jsonify({
            "productos": [producto.to_json() for producto in productos.items],
            "total": productos.total,
            "pages": productos.pages,
            "page": page
        })
        
      

class Producto(Resource):
    def get(self, id):
            try:
         
                producto = db.session.query(Productomodel).get_or_404(id)
                return producto.to_json()
            
            except:

                return make_response(jsonify({"error": f"Producto con id {id} no encontrado"}), 404)
            

    def put(self, id):
        producto = db.session.query(Productomodel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)

        try:

            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        
        except:
            return make_response(jsonify({"error": f"Producto con id {id} no modificado"}), 404)
        
    def delete(self, id):
        producto = db.session.query(Productomodel).get_or_404(id)

        try:

            db.session.delete(producto)
            db.session.commit()
            return make_response(jsonify({"success": f"Se ha eliminado el producto con id {id}"}))
        
        except:
            return make_response(jsonify({"error": f"No se pudo eliminar el id {id}"}))

            
          
         

