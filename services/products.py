# now we will access the data of the json file and run some basic operation of getting data from the database ...

import json
from pathlib import  Path
from typing import List,Dict

data_file = Path(__file__).parent.parent / "data" / "dummy.json"


def load_products()->List[Dict]:

    if not data_file.exists():
        return []
    with open(data_file,"r",encoding="utf-8") as f:
        return json.load(f)

def get_products()->List[Dict]:
    return load_products()

# if product is addable pass it through save_products then dump it to the file
def save_products(products:List[Dict])->None:
    with open(data_file,"w",encoding="utf-8") as f:
        json.dump(products,f,indent=2,ensure_ascii=False)

#load all the existing products and check if any common sku ,if yes raise value error,
# if not append it to the products and pass through save_products
def add_product(product:Dict)->Dict:
    products=get_products()
    if any(product["sku"]==p["sku"] for p in products):
        raise ValueError("sku already exists")
    products.append(product)
    save_products(products)
    return product

def remove_product(id:str)->str:
    products=get_products()
    for idx,p in enumerate(products):
        if p["id"]==str(id):
            deleted=products.pop(idx)
            save_products(products)
            return {"message":"product deleted","data":deleted}

def change_product(product_id:str,update_data:dict):
    products=get_products()
    for idx,p in enumerate(products):

        for key,value in update_data.items():
            if value is None:
                continue

            if isinstance(value,dict) and isinstance(p.get(key),dict):
                p[key].update(value)
            else:
                p[key]=value

        products[idx]=p
        save_products(p)
        return p

    raise ValueError("Product not found")

