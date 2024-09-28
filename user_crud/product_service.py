from product_repository import ProductRepository  # Importamos el repositorio de productos

class ProductService:
    
    @staticmethod
    def calculate_tax(product_price):
        """Calcula el impuesto sobre el precio del producto."""
        return product_price * (20 / 100)

    @staticmethod
    def calculate_total_price(product_price, tax_rate):
        """Calcula el precio total del producto incluyendo el impuesto."""
        tax = ProductService.calculate_tax(product_price, tax_rate)
        total_price = product_price + tax
        return total_price

    @staticmethod
    def get_product_by_field(field_name, value):
        # Se delega la búsqueda de productos por un campo específico al repositorio
        return ProductRepository.get_product_by_field(field_name, value)

    
    