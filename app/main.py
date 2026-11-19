from fastapi import FastAPI, HTTPException, Query, status
from typing import List, Optional
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.database import CatalogDatabase

app = FastAPI(title="E-Commerce Catalog Microservice", version="1.0.0")
db = CatalogDatabase()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "catalog-microservice"}

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(p: ProductCreate):
    return db.add_product(p.name, p.category, p.price, p.stock, p.description)

@app.get("/products", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None)
):
    return db.search_products(category=category, q=q)

@app.get("/products/{pid}", response_model=ProductResponse)
def get_product(pid: int):
    prod = db.get_product(pid)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@app.post("/products/{pid}/stock")
def update_stock(pid: int, delta: int = Query(..., description="Quantity to add or subtract")):
    updated = db.update_stock(pid, delta)
    if not updated:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return {"message": "Stock updated successfully", "product": updated}
