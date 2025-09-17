from sqlalchemy.orm import Session
from models import User, Product, Cart, Order
from schemas import UserCreate, ProductCreate, CartCreate, OrderCreate
from passlib.context import CryptContext
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Product CRUD
def get_products(db: Session, category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# Cart CRUD
def get_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, cart: CartCreate):
    db_cart = Cart(user_id=user_id, product_id=cart.product_id, quantity=cart.quantity)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
    return cart_item

def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
    return cart_item

# Order CRUD
def get_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def create_order(db: Session, user_id: int, order: OrderCreate):
    product = get_product(db, order.product_id)
    total_price = product.price * order.quantity
    db_order = Order(user_id=user_id, product_id=order.product_id, quantity=order.quantity, total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def checkout_cart(db: Session, user_id: int):
    cart_items = get_cart(db, user_id)
    orders = []
    for item in cart_items:
        order = create_order(db, user_id, OrderCreate(product_id=item.product_id, quantity=item.quantity))
        orders.append(order)
        remove_from_cart(db, user_id, item.product_id)
    return orders
