from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Base
from database import engine
from crud import *
from schemas import *
from auth import get_api_key

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API", version="1.0.0")

@app.get("/products", response_model=List[Product])
def read_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    products = get_products(db, category=category, min_price=min_price, max_price=max_price)
    return products

@app.post("/cart", response_model=Cart)
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    # Assume user_id is 1 for simplicity, in real app map from api_key
    user_id = 1
    return add_to_cart(db, user_id, cart)

@app.get("/cart", response_model=List[Cart])
def read_cart(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_id = 1
    return get_cart(db, user_id)

@app.put("/cart/{product_id}")
def update_cart(product_id: int, quantity: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_id = 1
    cart_item = update_cart_item(db, user_id, product_id, quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart updated"}

@app.delete("/cart/{product_id}")
def remove_cart(product_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_id = 1
    remove_from_cart(db, user_id, product_id)
    return {"message": "Item removed from cart"}

@app.post("/checkout", response_model=List[Order])
def checkout(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_id = 1
    orders = checkout_cart(db, user_id)
    return orders

@app.get("/orders", response_model=List[Order])
def read_orders(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_id = 1
    return get_orders(db, user_id)
