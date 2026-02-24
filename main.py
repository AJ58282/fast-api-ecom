from fastapi import FastAPI,HTTPException,Query
from services.products import get_products
from fastapi import Path
from schema.product import Product
app=FastAPI()
#app.get is for getting/fetching the data from the database etc.
#static route result remains the same
@app.get("/")
def root():
     return {"message":"Welcome to FastAPI"}

#dynamic route: value will change with input
# @app.get("/products/{id}")
# def product_id(id:int):
#      product=["Laptop","Camera","Brush"]
#      return product[id]

# @app.get("/products")
# def get_prod():
#      return get_products()

#we will use http exception to handle exceptions that occur such as 404,209 etc.
#when we run the Query function the link will also show the query passed eg: '/products?name=apple'
#we apply sort to sort asc or desc
@app.get('/products')
def list_products(name:str=Query(default=None,min_length=1,max_length=50,description="Search by product name"),
                  sort_price:bool=Query(default=False,description="Sort by product price"),
                  order:str=Query(default="asc",description="Sort by product when the sort_price=true {asc,desc}"),
                  limit:int=Query(default=5,ge=1,le=100,description="No. of products")):
     products=get_products()
     if name:
          new_name=name.lower().strip()
          products=[p for p in products if new_name in p.get('name','').lower()]
     if not products:
          raise HTTPException(status_code=404,detail=f"Product with name {name} not found")

     if sort_price:
          reverse=order=="desc"
          products= sorted(products,key=lambda p:p.get("price",0),reverse=reverse)

     products=products[:limit]
     total=len(products)

     return{
          "total_len":total,
          "items":products
     }

@app.get('/products/{product_id}')
def get_product_by_id(product_id:int=Path(...,ge=1,le=50,description="Search by product id",examples=1,)):
     products=get_products()
     prod=[p for p in products if p.get('id')==product_id]
     if not prod:
          raise HTTPException(status_code=404,detail=F"Product with id {product_id} not found")
     return prod[0]

#post used for getting/accepting the input data from the user which is used for some operation
#we have build a different file for the pydantic input validation stored in schema folder
@app.post('/products',status_code=201)
def create_product(product:Product):
     return product

