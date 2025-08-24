import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        color: #333 !important;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card h2 {
        color: #667eea !important;
        font-size: 2rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .metric-card p {
        color: #666 !important;
        font-size: 0.9rem;
        margin: 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    .product-card h2 {
        font-size: 3rem;
        margin: 0.5rem 0;
    }
    .product-card h4 {
        color: #333 !important;
        font-size: 1.2rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .product-card .price {
        color: #667eea !important;
        font-weight: bold;
        font-size: 1.3rem;
        margin: 0.5rem 0;
    }
    .product-card .rating {
        color: #ffa500 !important;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    .product-card .category {
        color: #666 !important;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    .info-box h4 {
        color: #333 !important;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .info-box p {
        color: #555 !important;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    .info-box strong {
        color: #333 !important;
        font-weight: 600;
    }
    .total-amount {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .total-amount h3 {
        color: white !important;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .total-amount h2 {
        color: white !important;
        font-size: 2rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .stDataFrame {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Service URLs
CATALOG_SERVICE_URL = "http://localhost:8001"
ACCOUNT_SERVICE_URL = "http://localhost:8002"
ORDER_SERVICE_URL = "http://localhost:8003"
CART_SERVICE_URL = "http://localhost:8004"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

def main():
    # Sidebar navigation
    st.sidebar.markdown("## 🛍️ E-Commerce Dashboard")
    st.sidebar.markdown("---")
    
    if not st.session_state.authenticated:
        st.sidebar.markdown("### 🔐 Authentication")
        auth_option = st.sidebar.selectbox(
            "Choose an option:",
            ["Login", "Register"]
        )
        
        if auth_option == "Login":
            show_login()
        else:
            show_register()
    else:
        st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.username}!")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📱 Navigation")
        page = st.sidebar.selectbox(
            "Select a page:",
            ["🏠 Dashboard", "📚 Catalog", "🛒 Cart", "📦 Orders"]
        )
        
        if page == "🏠 Dashboard":
            show_dashboard()
        elif page == "📚 Catalog":
            show_catalog()
        elif page == "🛒 Cart":
            show_cart()
        elif page == "📦 Orders":
            show_orders()

def show_login():
    st.markdown('<div class="main-header"><h1>🔐 User Login</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit_button:
                if username and password:
                    # Simulate authentication (replace with actual service call)
                    if username == "admin" and password == "admin":
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Login successful! Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.warning("⚠️ Please fill in all fields.")

def show_register():
    st.markdown('<div class="main-header"><h1>📝 User Registration</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            username = st.text_input("👤 Username", placeholder="Choose a username")
            email = st.text_input("📧 Email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Choose a password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit_button = st.form_submit_button("📝 Register", use_container_width=True)
            
            if submit_button:
                if username and email and password and confirm_password:
                    if password == confirm_password:
                        st.success("✅ Registration successful! You can now login.")
                    else:
                        st.error("❌ Passwords don't match!")
                else:
                    st.warning("⚠️ Please fill in all fields.")

def show_dashboard():
    st.markdown('<div class="main-header"><h1>🏠 Welcome to Your E-Commerce Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Products</h3>
            <h2>150+</h2>
            <p>Available items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🛒 Cart Items</h3>
            <h2>3</h2>
            <p>In your cart</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📦 Orders</h3>
            <h2>12</h2>
            <p>Total orders</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Total Spent</h3>
            <h2>$1,250</h2>
            <p>Lifetime value</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Recent Activity")
        activity_data = {
            "Activity": ["Product viewed", "Added to cart", "Order placed", "Review submitted"],
            "Time": ["2 min ago", "15 min ago", "1 hour ago", "2 hours ago"],
            "Details": ["iPhone 15 Pro", "MacBook Air", "Order #12345", "5-star rating"]
        }
        df = pd.DataFrame(activity_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🎯 Quick Actions")
        if st.button("🛒 View Cart", use_container_width=True):
            st.switch_page("Cart")
        if st.button("📚 Browse Catalog", use_container_width=True):
            st.switch_page("Catalog")
        if st.button("📦 Check Orders", use_container_width=True):
            st.switch_page("Orders")

def show_catalog():
    st.markdown('<div class="main-header"><h1>📚 Product Catalog</h1></div>', unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search products...", placeholder="Type to search...")
    
    with col2:
        category = st.selectbox("📂 Category", ["All", "Electronics", "Clothing", "Books", "Home"])
    
    with col3:
        sort_by = st.selectbox("🔄 Sort by", ["Price: Low to High", "Price: High to Low", "Name", "Rating"])
    
    st.markdown("---")
    
    # Sample products (replace with actual service call)
    products = [
        {"name": "iPhone 15 Pro", "price": 999, "category": "Electronics", "rating": 4.8, "image": "📱"},
        {"name": "MacBook Air M2", "price": 1199, "category": "Electronics", "rating": 4.9, "image": "💻"},
        {"name": "Nike Air Max", "price": 129, "category": "Clothing", "rating": 4.6, "image": "👟"},
        {"name": "Python Programming", "price": 49, "category": "Books", "rating": 4.7, "image": "📚"},
        {"name": "Coffee Maker", "price": 89, "category": "Home", "rating": 4.5, "image": "☕"},
        {"name": "Wireless Headphones", "price": 199, "category": "Electronics", "rating": 4.4, "image": "🎧"}
    ]
    
    # Display products in a grid
    cols = st.columns(3)
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h2>{product['image']}</h2>
                <h4>{product['name']}</h4>
                <p class="price">${product['price']}</p>
                <p class="rating">⭐ {product['rating']}/5.0</p>
                <p class="category">{product['category']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🛒 Add to Cart", key=f"add_{idx}", use_container_width=True):
                st.success(f"✅ {product['name']} added to cart!")

def show_cart():
    st.markdown('<div class="main-header"><h1>🛒 Shopping Cart</h1></div>', unsafe_allow_html=True)
    
    # Sample cart items (replace with actual service call)
    cart_items = [
        {"name": "iPhone 15 Pro", "price": 999, "quantity": 1, "image": "📱"},
        {"name": "MacBook Air M2", "price": 1199, "quantity": 1, "image": "💻"},
        {"name": "Wireless Headphones", "price": 199, "quantity": 2, "image": "🎧"}
    ]
    
    if not cart_items:
        st.info("🛒 Your cart is empty. Start shopping!")
        if st.button("📚 Browse Catalog", use_container_width=True):
            st.switch_page("Catalog")
    else:
        # Cart items table
        st.subheader("📋 Cart Items")
        
        cart_data = []
        total = 0
        
        for item in cart_items:
            item_total = item['price'] * item['quantity']
            total += item_total
            cart_data.append({
                "Product": f"{item['image']} {item['name']}",
                "Price": f"${item['price']}",
                "Quantity": item['quantity'],
                "Total": f"${item_total}"
            })
        
        df = pd.DataFrame(cart_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Summary and actions
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="total-amount">
                <h3>💰 Total Amount</h3>
                <h2>${total:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🚀 Quick Actions")
            if st.button("🛒 Update Cart", use_container_width=True):
                st.success("✅ Cart updated!")
            
            if st.button("💳 Proceed to Checkout", use_container_width=True):
                st.success("✅ Redirecting to checkout...")

def show_orders():
    st.markdown('<div class="main-header"><h1>📦 Order History</h1></div>', unsafe_allow_html=True)
    
    # Sample orders (replace with actual service call)
    orders = [
        {"id": "ORD-001", "date": "2024-01-15", "status": "Delivered", "total": 1199, "items": 2},
        {"id": "ORD-002", "date": "2024-01-10", "status": "Shipped", "total": 399, "items": 1},
        {"id": "ORD-003", "date": "2024-01-05", "status": "Delivered", "total": 89, "items": 1}
    ]
    
    if not orders:
        st.info("📦 No orders found. Start shopping to see your order history!")
        if st.button("📚 Browse Catalog", use_container_width=True):
            st.switch_page("Catalog")
    else:
        # Orders table
        st.subheader("📋 Recent Orders")
        
        order_data = []
        for order in orders:
            order_data.append({
                "Order ID": order['id'],
                "Date": order['date'],
                "Status": order['status'],
                "Items": order['items'],
                "Total": f"${order['total']}"
            })
        
        df = pd.DataFrame(order_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Order details
        st.subheader("📊 Order Details")
        selected_order = st.selectbox("Select an order to view details:", [order['id'] for order in orders])
        
        if selected_order:
            order = next((o for o in orders if o['id'] == selected_order), None)
            if order:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4>📋 Order Information</h4>
                        <p><strong>Order ID:</strong> {order['id']}</p>
                        <p><strong>Date:</strong> {order['date']}</p>
                        <p><strong>Status:</strong> {order['status']}</p>
                        <p><strong>Items:</strong> {order['items']}</p>
                        <p><strong>Total:</strong> ${order['total']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4>🚚 Shipping Status</h4>
                        <p><strong>Current Status:</strong> {order['status']}</p>
                        <p><strong>Estimated Delivery:</strong> 3-5 business days</p>
                        <p><strong>Tracking Number:</strong> TRK-{order['id']}</p>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
