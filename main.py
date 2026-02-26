import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID
from datetime import datetime
from typing import Dict, List

from db.session import get_db
from services.products import (
    get_all_products,
    add_product,
    remove_product,
    update_product
)
from schema.product import Product, ProductUpdate

load_dotenv()

app = FastAPI()

DB_PATH = os.getenv("BASE_URL")


# ---------------- ROOT ----------------
@app.get("/", response_model=Dict)
async def root():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to FastAPI",
            "Data_path": DB_PATH
        }
    )


# ---------------- GET ALL PRODUCTS ----------------
@app.get("/products")
async def list_products(
    name: str = Query(default=None, min_length=1, max_length=50),
    sort_price: bool = Query(default=False),
    order: str = Query(default="asc"),
    limit: int = Query(default=5, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    products = await get_all_products(db)

    # JSON mode returns list of dict
    # DB mode returns ORM objects
    if products and not isinstance(products[0], dict):
        products = [p.__dict__ for p in products]
        for p in products:
            p.pop("_sa_instance_state", None)

    if name:
        new_name = name.lower().strip()
        products = [
            p for p in products
            if new_name in p.get("name", "").lower()
        ]

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    if sort_price:
        reverse = order == "desc"
        products = sorted(
            products,
            key=lambda p: p.get("price", 0),
            reverse=reverse
        )

    products = products[:limit]

    return {
        "total_len": len(products),
        "items": products
    }


# ---------------- GET BY ID ----------------
@app.get("/products/{product_id}")
async def get_product_by_id(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    products = await get_all_products(db)

    if products and not isinstance(products[0], dict):
        products = [p.__dict__ for p in products]
        for p in products:
            p.pop("_sa_instance_state", None)

    prod = [p for p in products if str(p.get("id")) == str(product_id)]

    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    return prod[0]


# ---------------- CREATE ----------------
@app.post("/products", status_code=201)
async def create_product(
    product: Product,
    db: AsyncSession = Depends(get_db)
):
    product_dict = product.model_dump(mode="json")

    # JSON mode needs UUID
    if "id" not in product_dict:
        product_dict["id"] = str(uuid4())

    product_dict["created_at"] = datetime.utcnow().isoformat()

    try:
        created = await add_product(product_dict, db)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- DELETE ----------------
@app.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        deleted = await remove_product(product_id, db)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------------- UPDATE ----------------
@app.put("/products/{product_id}")
async def update_existing_product(
    product_id: str,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        updated = await update_product(
            product_id,
            payload.model_dump(mode="json", exclude_unset=True),
            db
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))