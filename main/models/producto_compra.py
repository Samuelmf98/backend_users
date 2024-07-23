from .. import db
import datetime as dt


class ProductoCompra(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    productoId = db.Column(db.Integer, db.ForeignKey("producto.id"), nullable = False)
    producto =db.relationship("Producto", back_populates = "productoscompras", uselist = False, single_parent = True)
    compraId = db.Column(db.Integer, db.ForeignKey("compra.id"), nullable = False)
    compra = db.relationship("Compra", back_populates = "productos_compras", uselist = False, single_parent = True)

    #back_populates="compras" asegura que la relación entre Usuario y Compra se mantenga consistente en ambos lados.
    #uselist = se devuelve un solo usuario asociado con cada compra y no una lista de usuarios.
    #single_parent=True implica que cada objeto Compra puede tener solo un objeto Usuario como su "padre" en el contexto de la relación.

    def __repr__(self):
        return f"Producto-compras: {self.id} {self.producto.to_json()} {self.compra.to_json()}"
    
    #Cuando enviamos un objeto python hay que convertirlo en json
    def to_json(self):
        productocompra_json = {

            "id" : self.id,
            "producto" : self.producto.to_json(),
            "compra": self.compra.to_json(),
        }

        return productocompra_json
    
    #Cuando recibamos un json tambien tiene que estar en formato python

    @staticmethod
    def from_json(productocompra_json):

        id = productocompra_json.get("id")
        productoId = productocompra_json.get("productoId")
        compraId = productocompra_json.get("compraId")
        
        return ProductoCompra(

            id = id,
            productoId = productoId,
            compraId = compraId,
        )