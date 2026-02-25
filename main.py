from fastapi import FastAPI,HTTPException,Query
from services.products import get_products, add_product,remove_product,change_product
from fastapi import Path
from schema.product import Product,ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
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
def get_product_by_id(product_id:int=Path(...,ge=1,le=50,description="Search by product id",examples=[1],)):
     products=get_products()
     prod=[p for p in products if p.get('id')==product_id]
     if not prod:
          raise HTTPException(status_code=404,detail=F"Product with id {product_id} not found")
     return prod[0]

#post used for getting/accepting the input data from the user which is used for some operation
#we have built a different file for the pydantic input validation stored in schema folder
#C aka create of CRUD operations
@app.post('/products',status_code=201)
def create_product(product:Product):
     product_dict=product.model_dump(mode="json")
     product_dict["id"]=str(uuid4())
     product_dict["created_at"]=datetime.utcnow().isoformat()
     try:
          add_product(product_dict)
     except ValueError as e:
          raise HTTPException(status_code=400,detail=str(e))
     return product.model_dump(mode="json")

#D aka delete of CRUD
@app.delete('/products/{product_id}')
def delete_product(product_id:UUID = Path(...,description="Delete product id",examples=[UUID("73cbdd06-5668-4e52-b172-e765f8468398")],)):
     try:
          del_val= remove_product(str(product_id))
          return del_val
     except ValueError as e:
          raise HTTPException(status_code=400,detail=str(e))

#U aks update of CRUD
#created update_product using a different pydantic class whether entries are optional
#payload:ProductUpdate where product update is the new class and payload is a parameter to call it
#exclude_unset is used to exclude variables which are not being passed in the function
@app.put('/products/{product_id}')
def update_product(
    product_id: UUID = Path(..., description="Update product"),
    payload: ProductUpdate = ...
):
    try:
        updated = change_product(
            str(product_id),
            payload.model_dump(mode="json", exclude_unset=True)
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

