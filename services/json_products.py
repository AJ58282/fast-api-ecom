import json
from pathlib import Path
from typing import List, Dict

data_file = Path(__file__).parent.parent / "data" / "dummy.json"


def load_products() -> List[Dict]:
    if not data_file.exists():
        return []
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_products(products: List[Dict]) -> None:
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


def get_all_products_json() -> List[Dict]:
    return load_products()


def add_product_json(product: Dict) -> Dict:
    products = load_products()

    if any(product["sku"] == p["sku"] for p in products):
        raise ValueError("SKU already exists")

    products.append(product)
    save_products(products)
    return product


def remove_product_json(product_id: str):
    products = load_products()

    for idx, p in enumerate(products):
        if p["id"] == str(product_id):
            deleted = products.pop(idx)
            save_products(products)
            return {"message": "product deleted", "data": deleted}

    raise ValueError("Product not found")


def update_product_json(product_id: str, update_data: Dict):
    products = load_products()

    for idx, p in enumerate(products):
        if p.get("id") == product_id:
            for key, value in update_data.items():
                if value is None:
                    continue
                p[key] = value

            products[idx] = p
            save_products(products)
            return p

    raise ValueError("Product not found")