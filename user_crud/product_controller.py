from flask_restful import Api, Resource
from product_repository import ProductRepository
from product_service import ProductService
from flask import Flask, app, request, jsonify, render_template 
from product import Product

from flask import Flask, render_template



def create_api(app):
    api = Api(app)

    class ProductResource(Resource):
        def get(self):
            products = ProductRepository.get_all_products()
            return [product.to_dict_product() for product in products]

        def post(self):
            data = request.get_json()
            new_product = ProductRepository.create_product(
                data['name'], data['description'], data['price'], data['stock'],
                data['image'], data['category']
            )
            return new_product.to_dict_product()

    class SingleProductResource(Resource):
        def get(self, product_id):
            product = ProductRepository.get_product_by_id(product_id)
            if product is None:
                return {'message': 'Product not found'}, 404
            return product.to_dict_product()

        def put(self, product_id):
            data = request.get_json()
            product = ProductRepository.update_product(product_id, **data)
            if product is None:
                return {'message': 'Product not found'}, 404
            return product.to_dict_product()

        def delete(self, product_id):
            product = ProductRepository.delete_product(product_id)
            if product is None:
                return {'message': 'Product not found'}, 404
            return {'message': 'Product deleted successfully'}
        
    


    class ProductByFieldResource(Resource):
        def get(self, field_name, value):
            # Verificamos que el campo sea válido antes de realizar la búsqueda
            valid_fields = ['name', 'description', 'price', 'category', 'stock', 'image']
            if field_name not in valid_fields:
                return {"message": "Campo inválido"}, 400  # Retornamos error si el campo no es válido
        
            # Obtenemos los productos por el campo específico
            products = ProductRepository.get_product_by_field(field_name, value)
        
        # Si encontramos productos, renderizamos el primer producto encontrado
            if products:
                product = products[0]  # Renderizamos solo el primer producto
                return render_template('product_detail.html', product=product)
            else:
                return {"message": "No se encontraron productos"}, 404  # Retornamos error si no se encuentran productos
        
        
     
        
    @app.route('/products', methods=['GET'])
    def show_products():
        products = ProductRepository.get_all_products()  # Obtén todos los productos
        return render_template('products.html', products=products)  # Renderiza la plantilla con los productos 
    
    
    @app.route('/products/search', methods=['GET'])
    def search_products():
        field_name = request.args.get('field_name')  # Obtener el campo de búsqueda
        value = request.args.get('value')  # Obtener el valor de búsqueda

        if not field_name or not value:
            return "Por favor, proporciona un campo y un valor de búsqueda", 400

    # Realiza la búsqueda utilizando el repositorio
        products = ProductRepository.get_product_by_field(field_name, value)

    # Renderiza la plantilla con los productos encontrados
        return render_template('products.html', products=products)
   

    # Ruta para mostrar los detalles de un producto
    @app.route('/products/<int:product_id>', methods=['GET'])
    def show_product_details(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        if product is None:
            return "Producto no encontrado", 404
        return render_template('product_detail.html', product=product)
    
    
    
    # Definimos las rutas para cada recurso
    api.add_resource(ProductResource, '/api/products')
    api.add_resource(SingleProductResource, '/products/<int:product_id>')
# Agregar la ruta para buscar productos por campo
    api.add_resource(ProductByFieldResource, '/api/products/search/<string:field_name>/<string:value>')
    return api