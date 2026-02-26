# services/products.py

from core.settings import USE_DATABASE
from services.json_products import (
    get_all_products_json,
    add_product_json,
    remove_product_json,
    update_product_json
)
from services.db_products import (
    get_all_products_db,
    add_product_db,
    update_product_db,
    delete_product_db
)


async def get_all_products(db=None):
    if USE_DATABASE:
        return await get_all_products_db(db)
    return get_all_products_json()


async def add_product(product_data: dict, db=None):
    if USE_DATABASE:
        return await add_product_db(product_data, db)
    return add_product_json(product_data)


async def update_product(product_id: str, update_data: dict, db=None):
    if USE_DATABASE:
        return await update_product_db(int(product_id), update_data, db)
    return update_product_json(product_id, update_data)


async def remove_product(product_id: str, db=None):
    if USE_DATABASE:
        return await delete_product_db(int(product_id), db)
    return remove_product_json(product_id)