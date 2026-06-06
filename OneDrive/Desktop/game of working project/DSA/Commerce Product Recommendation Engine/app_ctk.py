import customtkinter as ctk
from src.models import Product, User
from src.engine import RecommendationEngine

# --- 1. SETUP THE APP WINDOW ---
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ECommerceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("E-Commerce Recommendation Engine")
        self.geometry("900x600")

        # --- 2. INITIALIZE BACKEND ENGINE ---
        self.engine = RecommendationEngine()
        self.user = User("u1", "Guest User")
        self.engine.add_user(self.user)
        self.load_dummy_data()

        # --- 3. CONFIGURE UI GRID ---
        self.grid_columnconfigure(0, weight=2) # Left side (Catalog)
        self.grid_columnconfigure(1, weight=1) # Right side (Cart & Recs)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame: Catalog
        self.catalog_frame = ctk.CTkScrollableFrame(self, label_text="📦 Product Catalog", label_font=("Arial", 16, "bold"))
        self.catalog_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right Frame: Cart and Recommendations
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        self.cart_frame = ctk.CTkScrollableFrame(self.right_frame, label_text="🛍️ Your Cart", label_font=("Arial", 16, "bold"))
        self.cart_frame.grid(row=0, column=0, pady=(0, 5), sticky="nsew")

        self.recs_frame = ctk.CTkScrollableFrame(self.right_frame, label_text="✨ Recommended For You", label_font=("Arial", 16, "bold"), fg_color="#2b2b2b")
        self.recs_frame.grid(row=1, column=0, pady=(5, 0), sticky="nsew")

        # --- 4. RENDER INITIAL UI ---
        self.refresh_ui()

    def load_dummy_data(self):
        products = [
            Product("p1", "Mechanical Keyboard", "Electronics", 4.8),
            Product("p2", "Gaming Mouse", "Electronics", 4.5),
            Product("p3", "Python Crash Course", "Books", 4.9),
            Product("p4", "Clean Code", "Books", 4.7),
            Product("p5", "Running Shoes", "Apparel", 4.2),
            Product("p6", "Monitor Stand", "Electronics", 4.1),
        ]
        for p in products:
            self.engine.add_product(p)

    # --- 5. UI UPDATE LOGIC ---
    def refresh_ui(self):
        self.update_catalog()
        self.update_cart()
        self.update_recommendations()

    def update_catalog(self):
        # Clear existing widgets
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()

        # Populate products
        for pid, product in self.engine.catalog.items():
            if pid not in self.user.cart and pid not in self.user.purchased:
                card = ctk.CTkFrame(self.catalog_frame, corner_radius=10)
                card.pack(fill="x", padx=10, pady=5)

                name_lbl = ctk.CTkLabel(card, text=product.name, font=("Arial", 14, "bold"))
                name_lbl.pack(anchor="w", padx=10, pady=(5, 0))

                detail_lbl = ctk.CTkLabel(card, text=f"Category: {product.category} | Rating: {product.rating}★", text_color="gray")
                detail_lbl.pack(anchor="w", padx=10)

                # Action button using a lambda to pass the specific product ID
                btn = ctk.CTkButton(card, text="Add to Cart", width=100, command=lambda p=pid: self.add_to_cart(p))
                btn.pack(anchor="e", padx=10, pady=(0, 5))

    def update_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not self.user.cart:
            ctk.CTkLabel(self.cart_frame, text="Your cart is empty.", text_color="gray").pack(pady=10)
        else:
            for pid in self.user.cart:
                prod = self.engine.catalog[pid]
                ctk.CTkLabel(self.cart_frame, text=f"• {prod.name}").pack(anchor="w", padx=10, pady=2)
            
            buy_btn = ctk.CTkButton(self.cart_frame, text="🛒 Buy Now", fg_color="green", hover_color="darkgreen", command=self.buy_cart)
            buy_btn.pack(pady=15)

    def update_recommendations(self):
        for widget in self.recs_frame.winfo_children():
            widget.destroy()

        # Call the Priority Queue algorithm
        top_recs = self.engine.get_top_n_recommendations(self.user.user_id, n=3)

        if not top_recs:
            ctk.CTkLabel(self.recs_frame, text="Browse to get suggestions!", text_color="gray").pack(pady=10)
        else:
            for rank, (prod, score) in enumerate(top_recs, 1):
                card = ctk.CTkFrame(self.recs_frame, corner_radius=5, fg_color="#1f538d")
                card.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(card, text=f"#{rank} {prod.name}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(5,0))
                ctk.CTkLabel(card, text=f"Algo Score: {score:.1f}", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0,5))

    # --- 6. USER ACTIONS ---
    def add_to_cart(self, pid):
        self.user.add_to_cart(pid)
        self.refresh_ui()

    def buy_cart(self):
        self.user.buy_cart()
        self.refresh_ui()

if __name__ == "__main__":
    app = ECommerceApp()
    app.mainloop()