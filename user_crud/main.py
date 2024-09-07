from flask import Flask, request, jsonify  # Importamos Flask y herramientas para manejar solicitudes y respuestas en formato JSON
from user import db  # Importamos la base de datos desde el módulo 'user'
from user_controller import create_api  # Importamos la función que crea las rutas de la API desde 'user_controller'

app = Flask(__name__)  # Inicializamos la aplicación Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Configuramos la base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Deshabilitamos el rastreo de modificaciones para mejorar el rendimiento

db.init_app(app)  # Inicializamos la base de datos con la app Flask
app.request = request  # Vinculamos la solicitud HTTP al objeto app
app.jsonify = jsonify  # Vinculamos la función jsonify para retornar respuestas en JSON

with app.app_context():  # Dentro del contexto de la aplicación
    db.create_all()  # Creamos todas las tablas de la base de datos si no existen

api = create_api(app)  # Creamos las rutas de la API utilizando la función importada

if __name__ == '__main__':  # Si el script es ejecutado directamente
    app.run(debug=True)  # Iniciamos la aplicación en modo de depuración
