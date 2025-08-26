import streamlit as st
import pandas as pd
import json
from datetime import datetime
import re
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="TechMart - Premium Laptops",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background: white;
    }
    .price-tag {
        color: #e74c3c;
        font-size: 1.2em;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .order-summary {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #4caf50;
    }
    .product-view-modal {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #007bff;
        margin: 1rem 0;
    }
    .search-result-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .chat-product-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

class EcommerceBot:
    def __init__(self):
        self.products_df = self.load_products()
        if self.products_df.empty:
            self.products_df = self.create_sample_csv()
        self.initialize_session_state()
    
    def load_products(self):
        """Load products from CSV file"""
        try:
            return pd.read_csv('products.csv')
        except FileNotFoundError:
            st.error("Products CSV file not found. Please ensure 'products.csv' exists.")
            return pd.DataFrame()
    
    def create_sample_csv(self):
        """Create sample CSV data for fallback"""
        sample_data = {
            'id': list(range(1, 11)),
            'name': [
                'HP Pavilion Gaming 15', 'Dell Inspiron 15 3000', 'Lenovo ThinkPad E14', 'HP EliteBook 840 G8',
                'Dell XPS 13 9310', 'Lenovo Legion 5 15ACH6H', 'HP Spectre x360 14', 'Dell Latitude 5520',
                'Lenovo IdeaPad 3 15ITL6', 'HP Omen 15-en1013dx'
            ],
            'brand': ['HP', 'Dell', 'Lenovo', 'HP', 'Dell', 'Lenovo', 'HP', 'Dell', 'Lenovo', 'HP'],
            'category': [
                'Gaming Laptop', 'Budget Laptop', 'Business Laptop', 'Business Laptop', 'Ultrabook',
                'Gaming Laptop', '2-in-1 Laptop', 'Business Laptop', 'Budget Laptop', 'Gaming Laptop'
            ],
            'price': [425000, 365000, 520000, 685000, 735000, 615000, 695000, 465000, 385000, 575000],
            'stock_quantity': [15, 25, 12, 8, 6, 10, 7, 18, 22, 14],
            'specifications': [
                'Intel Core i5-11300H, 8GB RAM, 512GB SSD, NVIDIA GTX 1650, 15.6" FHD Display, Windows 11',
                'Intel Core i3-1115G4, 4GB RAM, 1TB HDD, Intel UHD Graphics, 15.6" HD Display, Windows 11',
                'Intel Core i5-1135G7, 8GB RAM, 256GB SSD, Intel Iris Xe Graphics, 14" FHD Display, Windows 11 Pro',
                'Intel Core i7-1165G7, 16GB RAM, 512GB SSD, Intel Iris Xe Graphics, 14" FHD Display, Windows 11 Pro',
                'Intel Core i7-1165G7, 16GB RAM, 512GB SSD, Intel Iris Xe Graphics, 13.3" 4K OLED Display, Windows 11',
                'AMD Ryzen 5 5600H, 8GB RAM, 512GB SSD, NVIDIA RTX 3060, 15.6" FHD 120Hz Display, Windows 11',
                'Intel Core i7-1165G7, 16GB RAM, 1TB SSD, Intel Iris Xe Graphics, 13.5" 3K2K OLED Touchscreen, Windows 11',
                'Intel Core i5-1135G7, 8GB RAM, 256GB SSD, Intel Iris Xe Graphics, 15.6" FHD Display, Windows 11 Pro',
                'Intel Core i3-1115G4, 4GB RAM, 1TB HDD, Intel UHD Graphics, 15.6" HD Display, Windows 11',
                'AMD Ryzen 7 5800H, 8GB RAM, 512GB SSD, NVIDIA RTX 3060, 15.6" FHD 144Hz Display, Windows 11'
            ],
            'image_url': [f'https://via.placeholder.com/300x200/{"0073e6" if brand == "HP" else "007DB8" if brand == "Dell" else "E2231A"}/FFFFFF?text={brand}+Laptop' 
                         for brand in ['HP', 'Dell', 'Lenovo', 'HP', 'Dell', 'Lenovo', 'HP', 'Dell', 'Lenovo', 'HP']]
        }
        return pd.DataFrame(sample_data)
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        session_vars = {
            'chat_history': [],
            'cart': [],
            'current_order': {},
            'user_name': None,
            'viewing_product': None,
            'redirect_to_checkout': False,
            'last_results': [],
            'show_search_results_buttons': False,
            'search_results_products': []
        }
        
        for key, default_value in session_vars.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def search_products(self, query: str) -> List[Dict]:
        """Search products based on query"""
        if self.products_df.empty:
            return []
        
        query_lower = query.lower()
        
        # Search in multiple columns
        mask = (
            self.products_df['name'].str.lower().str.contains(query_lower, na=False) |
            self.products_df['brand'].str.lower().str.contains(query_lower, na=False) |
            self.products_df['category'].str.lower().str.contains(query_lower, na=False) |
            self.products_df['specifications'].str.lower().str.contains(query_lower, na=False)
        )
        
        results = self.products_df[mask].to_dict('records')
        return results
    
    def format_price(self, price: float) -> str:
        """Format price in Nigerian Naira"""
        return f"₦{price:,.2f}"
    
    def process_user_message(self, message: str) -> str:
        """Process user message and generate bot response"""
        message_lower = message.lower()
        
        # Reset search results buttons when new message is processed
        st.session_state.show_search_results_buttons = False
        st.session_state.search_results_products = []
        
        # Handle name collection first
        if not st.session_state.user_name:
            if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
                return "Hello! Welcome to TechMart! 👋 What's your name?"
            
            # Try to extract name from various patterns
            name_patterns = [
                r"(?:my name is|i'm|i am|call me)\s+([a-zA-Z]+)",
                r"^([a-zA-Z]+)$",  # Just a single word (likely a name)
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    name = match.group(1).capitalize()
                    st.session_state.user_name = name
                    return f"Nice to meet you, {name}! 😊 I'm here to help you find the perfect laptop. You can ask me about our HP, Dell, or Lenovo laptops, or tell me what you're looking for."
            
            return "Could you please tell me your name? You can say 'My name is [Your Name]' or just type your name."
        
        # Greetings (after name is known)
        if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
            return f"Hello {st.session_state.user_name}! How can I help you find the perfect laptop today? 😊"
        
        # Product search
        if any(keyword in message_lower for keyword in ['laptop', 'hp', 'dell', 'lenovo', 'search', 'find', 'looking for', 'gaming', 'business', 'budget']):
            results = self.search_products(message)
            if results:
                st.session_state.last_results = results[:5]  # Store results for potential ordering
                st.session_state.show_search_results_buttons = True
                st.session_state.search_results_products = results[:5]
                
                response = f"Great choice, {st.session_state.user_name}! I found {len(results)} laptops that match your search:\n\n"
                for idx, product in enumerate(results[:5], 1):
                    response += f"{idx}. **{product['name']}**\n"
                    response += f"   Price: {self.format_price(product['price'])}\n"
                    response += f"   Stock: {product['stock_quantity']} units available\n\n"
                response += "You can use the buttons below to view details or add products to your cart!"
                return response
            else:
                return f"Sorry {st.session_state.user_name}, I couldn't find any laptops matching your search. Could you try different keywords? We have HP, Dell, and Lenovo laptops available."
        
        # Handle product ordering from search results
        if 'last_results' in st.session_state and st.session_state.last_results:
            for product in st.session_state.last_results:
                if any(word in message_lower for word in product['name'].lower().split()):
                    if 'add' in message_lower or 'cart' in message_lower or 'buy' in message_lower:
                        self.add_to_cart(product['id'])
                        return f"Perfect! I've added {product['name']} to your cart. Would you like to continue shopping or proceed to checkout?"
        
        # Price range queries
        price_match = re.search(r'(\d+)k?\s*-\s*(\d+)k?|under\s*(\d+)k?|below\s*(\d+)k?', message_lower)
        if price_match or 'price' in message_lower or 'cost' in message_lower or 'budget' in message_lower:
            return f"Great question, {st.session_state.user_name}! Our laptops range from ₦350,000 to ₦750,000. What's your budget range? I can help you find something perfect within your budget!"
        
        # Cart inquiries
        if 'cart' in message_lower or 'checkout' in message_lower:
            if st.session_state.cart:
                total = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
                response = f"Here's your cart, {st.session_state.user_name}:\n\n"
                for item in st.session_state.cart:
                    response += f"• {item['name']} x{item['quantity']} - {self.format_price(item['price'] * item['quantity'])}\n"
                response += f"\n**Total: {self.format_price(total)}**\n\nReady to checkout?"
                return response
            else:
                return f"Your cart is empty, {st.session_state.user_name}. Browse our products and add some laptops to your cart!"
        
        # Help
        if 'help' in message_lower:
            return f"""I'm here to help you, {st.session_state.user_name}! Here's what I can do:
            
            • Find laptops by brand (HP, Dell, Lenovo)
            • Search by specifications or price range
            • Help you add products to your cart
            • Provide product details and comparisons
            • Assist with your order
            
            Just ask me anything about our laptops!"""
        
        # Default response
        return f"I'm here to help you find the perfect laptop, {st.session_state.user_name}! You can ask me about specific brands, price ranges, or specifications. What are you looking for today?"
    
    def add_to_cart(self, product_id: int):
        """Add product to cart and redirect to checkout"""
        product = self.products_df[self.products_df['id'] == product_id].iloc[0]
        
        # Check if product already in cart
        for item in st.session_state.cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                st.success(f"Added another {product['name']} to cart!")
                st.session_state.redirect_to_checkout = True
                return
        
        # Add new item to cart
        cart_item = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'brand': product['brand']
        }
        st.session_state.cart.append(cart_item)
        st.success(f"Added {product['name']} to cart!")
        st.session_state.redirect_to_checkout = True
    
    def view_product(self, product_id: int):
        """Set product to view"""
        st.session_state.viewing_product = product_id
    
    def display_search_results_buttons(self):
        """Display interactive buttons for search results"""
        if st.session_state.show_search_results_buttons and st.session_state.search_results_products:
            st.markdown("### Quick Actions for Search Results")
            
            for product in st.session_state.search_results_products:
                with st.container():
                    st.markdown(f"""
                    <div class="search-result-card">
                        <h5>{product['name']}</h5>
                        <p><strong>Price:</strong> {self.format_price(product['price'])} | <strong>Stock:</strong> {product['stock_quantity']} units</p>
                        <p><small>{product['specifications'][:100]}...</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"View Details", key=f"search_view_{product['id']}", type="secondary"):
                            self.view_product(product['id'])
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Add to Cart", key=f"search_cart_{product['id']}", type="primary"):
                            self.add_to_cart(product['id'])
                            st.rerun()
                    
                    st.markdown("---")
    
    def display_product_view(self):
        """Display detailed product view"""
        if st.session_state.viewing_product:
            product = self.products_df[self.products_df['id'] == st.session_state.viewing_product].iloc[0]
            
            st.markdown(f"""
            <div class="product-view-modal">
                <h2>📱 {product['name']}</h2>
                <h4>Brand: {product['brand']}</h4>
                <h4>Category: {product['category']}</h4>
                <h3 class="price-tag">{self.format_price(product['price'])}</h3>
                <p><strong>Stock Available:</strong> {product['stock_quantity']} units</p>
                <h4>Full Specifications:</h4>
                <p>{product['specifications']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Add to Cart", key=f"view_cart_{product['id']}", type="primary"):
                    self.add_to_cart(product['id'])
                    st.rerun()
            
            with col2:
                if st.button("Close View", key=f"close_view_{product['id']}"):
                    st.session_state.viewing_product = None
                    st.rerun()
            
            with col3:
                if st.button("Back to Products", key=f"back_products_{product['id']}"):
                    st.session_state.viewing_product = None
                    st.rerun()
    
    def display_products_gallery(self):
        """Display products in a grid layout"""
        if self.products_df.empty:
            st.warning("No products available.")
            return
        
        # Show product view if selected
        if st.session_state.viewing_product:
            self.display_product_view()
            return
        
        # Show search results buttons if available
        if st.session_state.show_search_results_buttons:
            self.display_search_results_buttons()
            return
        
        st.markdown("### 🛍️ Our Premium Laptop Collection")
        
        # Create columns for product grid
        cols = st.columns(2)
        
        for idx, product in self.products_df.iterrows():
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="product-card">
                        <h4>{product['name']}</h4>
                        <p><strong>Brand:</strong> {product['brand']}</p>
                        <p><strong>Category:</strong> {product['category']}</p>
                        <p class="price-tag">{self.format_price(product['price'])}</p>
                        <p><strong>Stock:</strong> {product['stock_quantity']} units</p>
                        <p><small>{product['specifications'][:80]}...</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"Add to Cart", key=f"cart_{product['id']}", type="primary"):
                            self.add_to_cart(product['id'])
                            st.rerun()
                    with col2:
                        if st.button(f"View Details", key=f"view_{product['id']}"):
                            self.view_product(product['id'])
                            st.rerun()
    
    def display_chat_interface(self):
        """Display chat interface"""
        st.markdown("### 🤖 Chat with our AI Assistant")
        
        # Chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>Assistant:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input form (this will clear after submission)
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message here...", placeholder="Ask me about laptops, prices, or place an order!")
            submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            bot_response = self.process_user_message(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": bot_response})
            
            # Rerun to show new messages and clear input
            st.rerun()
    
    def display_cart_sidebar(self):
        """Display shopping cart in sidebar"""
        st.sidebar.markdown("### 🛒 Shopping Cart")
        
        # Show user name if available
        if st.session_state.user_name:
            st.sidebar.markdown(f"**Customer:** {st.session_state.user_name}")
            st.sidebar.markdown("---")
        
        if st.session_state.cart:
            total = 0
            for i, item in enumerate(st.session_state.cart):
                st.sidebar.markdown(f"**{item['name']}**")
                st.sidebar.markdown(f"Quantity: {item['quantity']}")
                st.sidebar.markdown(f"Price: {self.format_price(item['price'] * item['quantity'])}")
                
                if st.sidebar.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
                
                total += item['price'] * item['quantity']
                st.sidebar.markdown("---")
            
            st.sidebar.markdown(f"### Total: {self.format_price(total)}")
            
            if st.sidebar.button("Proceed to Checkout", type="primary"):
                st.session_state.redirect_to_checkout = True
                st.rerun()
            
            if st.sidebar.button("Clear Cart"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.sidebar.info("Your cart is empty")
        
        # Add a button to go back to all products
        if st.sidebar.button("🔙 Back to All Products"):
            st.session_state.show_search_results_buttons = False
            st.session_state.search_results_products = []
            st.session_state.viewing_product = None
            st.rerun()
    
    def display_checkout(self):
        """Display checkout form"""
        st.markdown("### 📋 Checkout")
        
        if not st.session_state.cart:
            st.warning("Your cart is empty. Add some products first!")
            return
        
        with st.form("checkout_form"):
            st.markdown("#### Customer Information")
            
            # Pre-fill name if available
            default_name = st.session_state.user_name if st.session_state.user_name else ""
            name = st.text_input("Full Name*", value=default_name, placeholder="Enter your full name")
            email = st.text_input("Email*", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number*", placeholder="+234 XXX XXX XXXX")
            address = st.text_area("Delivery Address*", placeholder="Enter your complete delivery address")
            
            st.markdown("#### Order Summary")
            total = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
            
            for item in st.session_state.cart:
                st.write(f"• {item['name']} x{item['quantity']} - {self.format_price(item['price'] * item['quantity'])}")
            
            st.markdown(f"**Total Amount: {self.format_price(total)}**")
            
            submitted = st.form_submit_button("Place Order", type="primary")
            
            if submitted:
                if name and email and phone and address:
                    # Create order record
                    order_data = {
                        'order_id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'customer_name': name,
                        'email': email,
                        'phone': phone,
                        'address': address,
                        'items': st.session_state.cart.copy(),
                        'total': total,
                        'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'Confirmed'
                    }
                    
                    # Save order (in real app, this would go to database)
                    st.success("🎉 Order placed successfully!")
                    st.markdown(f"""
                    <div class="order-summary">
                        <h4>Order Confirmation</h4>
                        <p><strong>Order ID:</strong> {order_data['order_id']}</p>
                        <p><strong>Customer:</strong> {name}</p>
                        <p><strong>Total:</strong> {self.format_price(total)}</p>
                        <p><strong>Status:</strong> Confirmed</p>
                        <p>Thank you for shopping with TechMart, {name}! You will receive a confirmation email shortly.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Clear cart and reset redirect flag
                    st.session_state.cart = []
                    st.session_state.redirect_to_checkout = False
                else:
                    st.error("Please fill in all required fields.")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🖥️ Emmanuel TechMart - Premium Laptops</h1>
        <p>Your one-stop shop for HP, Dell & Lenovo laptops</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize bot
    bot = EcommerceBot()
    
    # Sidebar for cart
    bot.display_cart_sidebar()
    
    # Handle redirect to checkout
    if st.session_state.get('redirect_to_checkout', False):
        # Create tabs but set checkout as default
        tab1, tab2 = st.tabs(["🛍️ Products & Chat", "🛒 Checkout"])
        
        # Auto-switch to checkout tab by showing it first
        with tab2:
            bot.display_checkout()
            # Reset redirect flag after showing checkout
            if st.button("Continue Shopping"):
                st.session_state.redirect_to_checkout = False
                st.rerun()
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                bot.display_products_gallery()
            
            with col2:
                bot.display_chat_interface()
    else:
        # Normal flow
        tab1, tab2 = st.tabs(["🛍️ Products & Chat", "🛒 Checkout"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                bot.display_products_gallery()
            
            with col2:
                bot.display_chat_interface()
        
        with tab2:
            bot.display_checkout()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>TechMart - Premium Laptops powered with AI Assistants </p>
        <p>For support, contact us at: support@techmart.ng</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()