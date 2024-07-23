from .. import db
import datetime as dt


class Compra(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    fecha_compra = db.Column(db.DateTime, default = dt.datetime.now(), nullable = False)
    usuarioId =db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)
    usuario =db.relationship("Usuario", back_populates = "compras", uselist = False, single_parent = True)
    productos_compras = db.relationship("ProductoCompra", back_populates = "compra", cascade = "all, delete-orphan")
 
    def __repr__(self):
        return f"compra: {self.id} {self.usuarioId}"
    
    #Cuando recibimos de la base de datos un objeto python hay que convertirlo en json
    def to_json(self):
        compra_json = {

            "id" : self.id,
            "fecha_compra" : str(self.fecha_compra),
            "usuario": self.usuario.to_json()
        }

        return compra_json
    
    #Cuando enviamos un un json a la base de datos, tiene primero que convertirse a formato python

    @staticmethod
    def from_json(compra_json):

        id = compra_json.get("id")
        fecha_compra = compra_json.get("fecha_compra")
        usuarioId = compra_json.get("usuarioId")

        
        return Compra(

            id = id,
            fecha_compra = fecha_compra,
            usuarioId = usuarioId,
        )