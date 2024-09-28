from product import Product  # Importamos el modelo Product
from user import db  # Importamos la base de datos desde el módulo 'user'

class ProductRepository:
    
    @staticmethod
    def get_all_products():
        """Obtiene todos los productos desde la base de datos."""
        return Product.query.all()  # Obtenemos todos los productos

    @staticmethod
    def get_product_by_id(product_id):
        """Obtiene un producto por su ID."""
        return Product.query.get(product_id)  # Obtenemos un producto por su ID

    @staticmethod
    def get_product_by_field(field_name, value):
        """Filtra productos por un campo específico."""
        return Product.query.filter(getattr(Product, field_name) == value).all()  # Filtramos productos

    @staticmethod
    def create_product(name, description, price, stock, image, category):
        """Crea un nuevo producto en la base de datos."""
        new_product = Product(
            name=name, 
            description=description, 
            price=price, 
            stock=stock, 
            image=image, 
            category=category
        )
        db.session.add(new_product)  # Agregamos el nuevo producto a la sesión
        db.session.commit()  # Guardamos los cambios en la base de datos
        return new_product

    @staticmethod
    def update_product(product_id, name=None, description=None, price=None, stock=None, image=None, category=None):
        """Actualiza un producto existente en la base de datos."""
        product = Product.query.get(product_id)  # Obtenemos el producto por su ID
        if product:
            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if stock:
                product.stock = stock
            if image:
                product.image = image
            if category:
                product.category = category
            db.session.commit()  # Guardamos los cambios
        return product

    @staticmethod
    def delete_product(product_id):
        """Elimina un producto de la base de datos."""
        product = Product.query.get(product_id)  # Obtenemos el producto por su ID
        if product:
            db.session.delete(product)  # Eliminamos el producto
            db.session.commit()  # Guardamos los cambios
        return product
