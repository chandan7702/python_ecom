from database import SessionLocal
from models import Product, User
from crud import create_user
from schemas import UserCreate, ProductCreate

db = SessionLocal()

# Create sample user
user = UserCreate(username="testuser", email="test@example.com", password="password")
create_user(db, user)

# Create sample products
products = [
    ProductCreate(name="Laptop", description="A powerful laptop", price=999.99, stock_quantity=10, category="Electronics", image_url="http://example.com/laptop.jpg"),
    ProductCreate(name="Book", description="A great book", price=19.99, stock_quantity=50, category="Books", image_url="http://example.com/book.jpg"),
    ProductCreate(name="Shoes", description="Comfortable shoes", price=49.99, stock_quantity=20, category="Clothing", image_url="http://example.com/shoes.jpg"),
]

for p in products:
    db_product = Product(**p.dict())
    db.add(db_product)

db.commit()
db.close()

print("Sample data inserted.")
