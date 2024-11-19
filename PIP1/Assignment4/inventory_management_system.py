from datetime import date

class Product:
    def __init__(self, productID, name, price, stockQuantity, supplier):
        self.productID = productID
        self.name = name
        self.price = price
        self.stockQuantity = stockQuantity
        self.supplier = supplier

    def update_stock(self, quantity):
        self.stockQuantity += quantity
        print(f"Updated stock for {self.name}. New quantity: {self.stockQuantity}")

    def check_availability(self):
        return self.stockQuantity > 0

    def __str__(self):
        return f"Product[ID={self.productID}, Name={self.name}, Price={self.price}, Stock={self.stockQuantity}, Supplier={self.supplier.name}]"

class Supplier:
    def __init__(self, supplierID, name, address):
        self.supplierID = supplierID
        self.name = name
        self.address = address
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def view_products(self):
        for product in self.products:
            print(product)

    def __str__(self):
        return f"Supplier[ID={self.supplierID}, Name={self.name}, Address={self.address}]"

class Order:
    def __init__(self, orderID, product, quantity, orderDate=date.today()):
        self.orderID = orderID
        self.product = product
        self.quantity = quantity
        self.orderDate = orderDate

    def calculate_total_cost(self):
        return self.quantity * self.product.price

    def fulfill_order(self):
        self.product.update_stock(self.quantity)
        print(f"Order fulfilled. Product: {self.product.name}, Quantity: {self.quantity}")

    def __str__(self):
        return f"Order[ID={self.orderID}, Product={self.product.name}, Quantity={self.quantity}, Date={self.orderDate}]"

class Warehouse:
    def __init__(self, warehouseID, location):
        self.warehouseID = warehouseID
        self.location = location
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def __str__(self):
        return f"Warehouse[ID={self.warehouseID}, Location={self.location}]"

class Store:
    def __init__(self):
        self.products = []
        self.suppliers = []
        self.orders = []
        self.warehouses = []

    def add_product(self, product):
        self.products.append(product)

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)

    def add_order(self, order):
        self.orders.append(order)

    def add_warehouse(self, warehouse):
        self.warehouses.append(warehouse)

    def search_product(self, productID):
        for product in self.products:
            if product.productID == productID:
                return product
        return None

    def search_supplier(self, supplierID):
        for supplier in self.suppliers:
            if supplier.supplierID == supplierID:
                return supplier
        return None

    def search_order(self, orderID):
        for order in self.orders:
            if order.orderID == orderID:
                return order
        return None

# Testing the system with objects

# Create suppliers
supplier1 = Supplier(supplierID=1, name="Global Supplies Inc.", address="123 Main St")
supplier2 = Supplier(supplierID=2, name="Local Distributors", address="456 Market Ave")

# Create products and link them to suppliers
product1 = Product(productID=101, name="Laptop", price=1000.00, stockQuantity=10, supplier=supplier1)
product2 = Product(productID=102, name="Keyboard", price=50.00, stockQuantity=50, supplier=supplier2)

# Link products to suppliers
supplier1.add_product(product1)
supplier2.add_product(product2)

# Create a warehouse and add products to it
warehouse1 = Warehouse(warehouseID=1, location="North Warehouse")
warehouse1.add_product(product1)
warehouse1.add_product(product2)

# Create a store and add entities to it
store = Store()
store.add_product(product1)
store.add_product(product2)
store.add_supplier(supplier1)
store.add_supplier(supplier2)
store.add_warehouse(warehouse1)

# Create an order and fulfill it
order1 = Order(orderID=1, product=product1, quantity=5)
store.add_order(order1)
print(f"Order Total Cost: ${order1.calculate_total_cost()}")
order1.fulfill_order()

# Search functionality
print("Searching for Product ID 101:")
print(store.search_product(101))

print("Searching for Supplier ID 2:")
print(store.search_supplier(2))

print("Searching for Order ID 1:")
print(store.search_order(1))
