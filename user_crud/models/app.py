
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Product, Cart  # Asegúrate de tener un modelo de Cart (Carrito) configurado


# Configuración de Flask y SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'  # Usando SQLite para almacenar productos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'  # Para manejar las sesiones de usuario
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para mostrar mensajes flash

db = SQLAlchemy(app)
db = SQLAlchemy()


# Modelo de Producto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

# Ruta para la lista de productos con búsqueda

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('Product', secondary='cart_product', backref='carts')

    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
            db.session.commit()

class CartProduct(db.Model):
    __tablename__ = 'cart_product'
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
@app.route('/products', methods=['GET'])
def products():
    field_name = request.args.get('field_name', None)
    value = request.args.get('value', None)

    if field_name and value:
        # Si se pasa un parámetro de búsqueda, filtramos los productos
        products = Product.query.filter(getattr(Product, field_name).like(f"%{value}%")).all()
    else:
        # Si no hay parámetros de búsqueda, mostramos todos los productos
        products = Product.query.all()

    return render_template('product.html', products=products)

# Ruta para agregar productos al carrito
@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Crear un carrito en la sesión si no existe
    if 'cart' not in session:
        session['cart'] = []

    # Añadir el producto al carrito
    session['cart'].append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': 1  # Suponiendo que agregamos 1 unidad por defecto
    })
    
    # Guardar el carrito en la sesión
    session.modified = True

    return redirect(url_for('products'))

# Ruta para ver el carrito
@app.route('/cart', methods=['GET'])
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


# Ruta para agregar al carrito
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Lógica para agregar el producto al carrito (esto asume que ya tienes un modelo de carrito)
    cart = Cart.query.first()  # Asumiendo que solo hay un carrito en el sistema
    cart.add_product(product)

    # Mostrar mensaje de confirmación
    flash(f'El producto {product.name} ha sido agregado al carrito.')

    return redirect(url_for('cart'))

# Ruta para mostrar los productos en el carrito
@app.route('/cart')
def cart():
    cart = Cart.query.first()  # Asumimos un solo carrito
    return render_template('cart.html', cart=cart)

if __name__ == "__main__":
    app.run(debug=True)
# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
