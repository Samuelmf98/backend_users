import os 
from dotenv import load_dotenv #variables de entorno
from flask import Flask
from flask_restful import Api #para crear la api-rest
from flask_sqlalchemy import SQLAlchemy


api = Api()

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    '''A continuacion veremos como crear el archivo de sqlite que será nuestra 
    base de datos, este archivo se tendrá que borrar y crear cada vez que nosotros hagamos
    un cambio que afecte a la base de datos'''

    #Cargamos variables de entorno (Una carpeta hacias atras)
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path=dotenv_path)

    #Configuracion de la base de datos
    PATH = os.getenv("DATABASE_PATH")
    NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f"{PATH}{NAME}"):
        os.chdir(f"{PATH}")
        file = os.open(f"{NAME}", os.O_CREAT) #si no existe que cree el archivo y luego lo podemos arbrir con Dbeaver

    #Para que la base de datos registre en todo momento los cambios que se hacen
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    #Comando para hacer la conexion
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH}{NAME}"
    db.init_app(app)


    import main.resources as resources
    api.add_resource(resources.UsuariosResource, "/usuarios")
    api.add_resource(resources.UsuarioResource, "/usuario/<id>")
    api.add_resource(resources.ComprasResource, "/compras")
    api.add_resource(resources.CompraResource, "/compra/<id>")
    api.add_resource(resources.ProductosResource, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<id>")
    api.add_resource(resources.ProductosComprasResource, "/productos_compras")
    api.add_resource(resources.ProductoCompraResource, "/producto_compra/<id>")

    api.init_app(app)

    return app