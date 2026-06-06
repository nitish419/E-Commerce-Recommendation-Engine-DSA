# main.py

# Import the classes from your modular files
from src.models import Product, User
from src.engine import RecommendationEngine

def run_simulation():
    engine = RecommendationEngine()

    # 1. Create Catalog
    products = [
        Product("p1", "Mechanical Keyboard", "Electronics", 4.8),
        Product("p2", "Gaming Mouse", "Electronics", 4.5),
        Product("p3", "Python Crash Course", "Books", 4.9),
        Product("p4", "Clean Code", "Books", 4.7),
        Product("p5", "Running Shoes", "Apparel", 4.2),
        Product("p6", "Monitor Stand", "Electronics", 4.1),
    ]
    for p in products:
        engine.add_product(p)

    # 2. Create User
    u1 = User("u1", "Alex")
    engine.add_user(u1)

    print("--- E-COMMERCE RECOMMENDATION ENGINE ---")
    print("Simulating User Activity...\n")

    # 3. Simulate activity
    u1.view_history.extend(["p1", "p6"])
    u1.add_to_cart("p2")

    print(f"User: {u1.name}")
    print(f"Current Cart: {[engine.catalog[pid].name for pid in u1.cart]}")
    print("-" * 40)

    # 4. Generate Recommendations
    print("Generating Top 3 Recommendations...\n")
    top_recs = engine.get_top_n_recommendations("u1", n=3)

    for rank, (prod, score) in enumerate(top_recs, 1):
        print(f"Rank {rank}: {prod.name} | Category: {prod.category} | Algo Score: {score:.1f}")

    print("-" * 40)
    
    # 5. Simulate Purchase and Re-run Engine
    print("User buys the cart items...")
    u1.buy_cart()
    print("Generating new recommendations (Purchased items filtered out)...\n")
    
    new_recs = engine.get_top_n_recommendations("u1", n=3)
    for rank, (prod, score) in enumerate(new_recs, 1):
        print(f"Rank {rank}: {prod.name} | Category: {prod.category} | Algo Score: {score:.1f}")

if __name__ == "__main__":
    run_simulation()