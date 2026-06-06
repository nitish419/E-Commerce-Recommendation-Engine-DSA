# app.py
import streamlit as st
from src.models import Product, User
from src.engine import RecommendationEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Product Recommendations", page_icon="🛒", layout="wide")
st.title("🛒 E-Commerce Recommendation Engine (DSA Proof of Work)")

# --- PERSIST BACKEND STATE ---
if 'engine' not in st.session_state:
    engine = RecommendationEngine()
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
    st.session_state.engine = engine

if 'user' not in st.session_state:
    user = User("u1", "Verified Candidate")
    st.session_state.engine.add_user(user)
    st.session_state.user = user

engine = st.session_state.engine
user = st.session_state.user

# --- LAYOUT DESIGN ---
col_catalog, col_sidebar = st.columns([2, 1])

with col_catalog:
    st.header("📦 Available Products")
    grid = st.columns(3)
    
    for i, (pid, product) in enumerate(engine.catalog.items()):
        if pid not in user.cart and pid not in user.purchased:
            with grid[i % 3]:
                st.subheader(product.name)
                st.caption(f"Category: {product.category}")
                st.write(f"Rating: {product.rating} ★")
                if st.button(f"Add to Cart", key=f"web_add_{pid}"):
                    user.add_to_cart(pid)
                    st.rerun()

with col_sidebar:
    st.header("🛍️ Active Shopping Cart")
    if not user.cart:
        st.info("Your shopping cart is empty.")
    else:
        for pid in user.cart:
            item = engine.catalog[pid]
            st.write(f"• **{item.name}** ({item.category})")
        
        if st.button("Proceed to Checkout", type="primary"):
            user.buy_cart()
            st.success("Purchase processed successfully!")
            st.rerun()

    st.divider()
    st.header("✨ Priority Queue Recommendations")
    
    # Fire backend heap/priority-queue engine
    top_recs = engine.get_top_n_recommendations(user.user_id, n=3)
    
    if not top_recs:
        st.write("Add items or checkout to view hyper-targeted suggestions.")
    else:
        for rank, (prod, score) in enumerate(top_recs, 1):
            st.info(f"**#{rank} {prod.name}**\n\nCategory: {prod.category} | Algo Score: {score:.1f}")