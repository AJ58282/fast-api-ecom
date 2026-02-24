# now we will acess the data of the json file and run some basic operation of getting data from the database ...

import json
from pathlib import  Path
from typing import List,Dict

def load_products()->List[Dict]:
    data_file=Path(__file__).parent.parent/"data"/"products.json"

    if not data_file.exists():
        return []
    with open(data_file,"r",encoding="utf-8") as f:
        return json.load(f)

def get_products()->List[Dict]:
    return load_products()