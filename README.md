# E-commerce API

A basic e-commerce application built with FastAPI and MySQL.

## Features

- Product listing with filtering
- Cart management
- Order processing
- User authentication (API key)

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up MySQL database:
   - Create a MySQL database named `ecommerce`.
   - Run the schema.sql to create tables.

3. Set environment variable for DATABASE_URL:
   ```
   export DATABASE_URL="mysql+pymysql://user:password@localhost/ecommerce"
   ```

4. Run sample data script:
   ```
   python sample_data.py
   ```

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /products` - List products with optional filters
- `POST /cart` - Add to cart
- `GET /cart` - View cart
- `PUT /cart/{product_id}` - Update cart item
- `DELETE /cart/{product_id}` - Remove from cart
- `POST /checkout` - Checkout cart
- `GET /orders` - View orders

Use API key: `mysecretapikey` in header `access_token`.

## Deployment on Railway

1. Create a Railway account at https://railway.app.

2. Create a new project.

3. Add a MySQL database service.

4. Deploy the app:
   - Connect GitHub repo or upload code.
   - Set environment variables: DATABASE_URL from Railway MySQL.

5. Railway will provide the URL for the deployed app.
