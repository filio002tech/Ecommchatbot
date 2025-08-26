# E-commerce Laptop Bot - TechMart

A complete e-commerce chatbot application built with Streamlit and Python, featuring an AI assistant for laptop sales.

## Features

- 🛍️ **E-commerce Interface**: Professional product gallery with 50+ laptops
- 🤖 **AI Chat Assistant**: Intelligent chatbot for customer service and product recommendations
- 🛒 **Shopping Cart**: Add/remove products, manage quantities, and checkout
- 📊 **Product Search**: Search by brand, price range, specifications
- 💳 **Order Processing**: Complete checkout flow with order confirmation
- 📱 **Responsive Design**: Mobile-friendly interface

## Product Inventory

- **50 Laptop Products** from HP, Dell, and Lenovo
- **Price Range**: ₦350,000 - ₦750,000 (Nigerian Naira)
- **Categories**: Gaming, Business, Budget, Ultrabook, Workstation, 2-in-1
- **Stock Management**: Real-time inventory tracking

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ecommerce-laptop-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - Local URL: http://localhost:8501

### File Structure

```
ecommerce-laptop-bot/
├── app.py                 # Main Streamlit application
├── products.csv           # Product database (50 laptops)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Deployment on Streamlit Cloud

### Method 1: Direct GitHub Integration

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

### Method 2: Using Streamlit Cloud Dashboard

1. Visit [streamlit.io](https://streamlit.io)
2. Sign up/Login with GitHub
3. Click "New App"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Deploy!"

## Chatbot Capabilities

The AI assistant can:

- **Product Search**: Find laptops by brand, specifications, or price range
- **Price Queries**: Answer questions about pricing and budget ranges
- **Product Comparison**: Compare different laptop models
- **Order Assistance**: Help customers add products to cart and checkout
- **Customer Service**: Answer general questions about products and policies
- **Stock Information**: Provide real-time stock availability

### Example Interactions

- "Show me HP laptops under 500k"
- "I need a gaming laptop with RTX 3060"
- "What's the difference between Dell XPS and Inspiron?"
- "Add the Lenovo ThinkPad to my cart"
- "What laptops do you have for business use?"

## Customization Options

### Adding New Products

1. Edit `products.csv` file
2. Add new rows with required columns:
   - id, name, brand, category, price, stock_quantity, specifications, image_url

### Modifying Chat Responses

1. Edit the `process_user_message()` method in `app.py`
2. Add new keywords and response patterns
3. Customize greeting messages and product descriptions

### Styling Changes

1. Modify CSS in the `st.markdown()` sections
2. Update color schemes and layout
3. Change fonts and spacing

## Technical Details

### Dependencies

- **Streamlit**: Web framework for the interface
- **Pandas**: Data manipulation and CSV handling
- **Python 3.8+**: Programming language

### Database

- **CSV File**: Simple file-based product storage
- **In-Memory**: Cart and session data stored in Streamlit session state
- **Scalable**: Can easily migrate to SQL database

### AI Features

- **Natural Language Processing**: Basic keyword matching and pattern recognition
- **Product Search**: Multi-column text search functionality
- **Context Awareness**: Maintains conversation history and user preferences

## Production Considerations

### For Production Deployment

1. **Database**: Migrate from CSV to PostgreSQL/MySQL
2. **Authentication**: Add user login and registration
3. **Payment Gateway**: Integrate Paystack, Flutterwave, or Stripe
4. **Email Service**: Add order confirmation emails
5. **Analytics**: Track user behavior and sales metrics
6. **Security**: Add HTTPS, input validation, and rate limiting

### Scaling Options

- **Database**: PostgreSQL with connection pooling
- **File Storage**: AWS S3 or Cloudinary for product images
- **Deployment**: Docker containers with load balancing
- **Monitoring**: Add logging and error tracking

## Environment Variables

For production, set these environment variables:

```bash
# Optional configurations
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Support and Development

### Adding New Features

1. **Inventory Management**: Admin panel for product management
2. **User Accounts**: Customer profiles and order history
3. **Advanced Search**: Filters, sorting, and faceted search
4. **Recommendations**: ML-based product recommendations
5. **Reviews**: Customer ratings and reviews system

### Troubleshooting

- **CSV File Not Found**: Ensure `products.csv` is in the same directory as `app.py`
- **Port Already in Use**: Change port with `streamlit run app.py --server.port 8502`
- **Module Not Found**: Install requirements with `pip install -r requirements.txt`

## Demo Data

The included CSV contains 50 realistic laptop products with:
- **Brands**: HP (17 models), Dell (17 models), Lenovo (16 models)
- **Categories**: Gaming, Business, Budget, Ultrabook, Workstation, 2-in-1
- **Price Range**: ₦350,000 - ₦750,000
- **Specifications**: Detailed hardware specs for each model

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please contact the development team.

---

**TechMart E-commerce Bot** - Your AI-powered laptop shopping assistant! 🖥️✨