
from flask import Flask, request, jsonify, render_template
from user import db  # Importamos la base de datos desde el módulo 'user'

from user_repository import UserRepository
from product import Product  # Solo importas el modelo Product, no es necesario importar db otra vez

from product_repository import ProductRepository

from user_controller import create_api as create_user_api  # Importamos la función que crea las rutas de la API para usuarios
from product_controller import create_api as create_product_api  # Importamos la función que crea las rutas de la API para productos




app = Flask(__name__)  # Inicializamos la aplicación Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Configuramos la base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Deshabilitamos el rastreo de modificaciones para mejorar el rendimiento

db.init_app(app)  # Inicializamos la base de datos con la app Flask
app.request = request  # Vinculamos la solicitud HTTP al objeto app
app.jsonify = jsonify  # Vinculamos la función jsonify para retornar respuestas en JSON

with app.app_context():  # Dentro del contexto de la aplicación
    db.create_all()  # Creamos todas las tablas de la base de datos si no existen



create_user_api(app)  # Crea las rutas de la API para usuarios
create_product_api(app)  # Crea las rutas de la API para productos


if __name__ == '__main__':  # Si el script es ejecutado directamente
    app.run(debug=True)  # Iniciamos la aplicación en modo de depuración
