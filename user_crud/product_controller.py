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
        
        
     
        
    @app.route('/products', methods=['GET'])
    def show_products():
        products = ProductRepository.get_all_products()  # Obtén todos los productos
        return render_template('products.html', products=products)  # Renderiza la plantilla con los productos    

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

    return api