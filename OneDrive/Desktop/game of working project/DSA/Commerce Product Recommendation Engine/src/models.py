# src/models.py

class Product:
    def __init__(self, product_id, name, category, rating):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.rating = rating  # 0.0 to 5.0

    def __repr__(self):
        return f"{self.name} ({self.category}) - {self.rating}★"

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.view_history = []  # List of product IDs viewed
        self.cart = set()       # Set of product IDs in cart for O(1) lookup
        self.purchased = set()  # Set of purchased product IDs

    def add_to_cart(self, product_id):
        self.cart.add(product_id)

    def buy_cart(self):
        self.purchased.update(self.cart)
        self.cart.clear()