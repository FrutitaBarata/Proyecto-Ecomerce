from flask_sqlalchemy import SQLAlchemy  # Importamos SQLAlchemy para manejar la base de datos
from user import db


class Product(db.Model):
    __tablename__ = 'products'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID del producto, clave primaria
    name = db.Column(db.String(100), nullable=False)  # Nombre del producto, obligatorio
    description = db.Column(db.String(255), nullable=True)  # Descripción del producto, opcional
    price = db.Column(db.Float, nullable=False)  # Precio del producto, obligatorio
    stock = db.Column(db.Integer, nullable=False, default=0)  # Cantidad en stock del producto
    image = db.Column(db.String(255), nullable=True)  # Imagen del producto, opcional
    category = db.Column(db.String(50), nullable=False)  # Categoría del producto

    def to_dict_product(self):
        """Convierte el modelo a un diccionario para serialización."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
            "category": self.category
        }
