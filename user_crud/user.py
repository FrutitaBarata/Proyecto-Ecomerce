from flask_sqlalchemy import SQLAlchemy  # Importamos SQLAlchemy para manejar la base de datos

db = SQLAlchemy()  # Inicializamos el objeto de base de datos

class User(db.Model):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID del usuario, clave primaria
    name = db.Column(db.String(80), nullable=False)  # Nombre del usuario, obligatorio
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario, único y obligatorio
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email del usuario, único y obligatorio
    password = db.Column(db.String(120), nullable=False)  # Contraseña del usuario, obligatoria
    updated_at =  db.Column(db.String(120), nullable=False)  # Fecha de actualización del perfil
    image = db.Column(db.String(255), nullable=True)  # Imagen del perfil del usuario, opcional
    rol = db.Column(db.String(50), nullable=False)  # Rol del usuario, obligatorio
