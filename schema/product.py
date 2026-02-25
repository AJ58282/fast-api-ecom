#AnyUrl is used to get url as input with the help of pydantic
#Literal is used to fix the value of an attribute
#for validating single field we will use field validator eg:sku=abc-def-jhi the input needs
# the hyphen also we will check for it to.


from pydantic import BaseModel, Field,field_validator,model_validator,computed_field,AnyUrl,EmailStr
from typing import Annotated, Literal
from uuid import UUID
from datetime import datetime

from pydantic import EmailStr


class Dimension(BaseModel):
    length:Annotated[float,Field(gt=0,lt=100,description="length of product/device")]
    width:Annotated[float,Field(gt=0,lt=50,description="width of product/device")]
    height:Annotated[float,Field(gt=0,lt=50,description="height of product/device")]



class Seller(BaseModel):
    seller_id: UUID
    name:Annotated[str,Field(description="Seller name")]
    email:EmailStr
    website:AnyUrl

    @field_validator("email",mode="after")
    @classmethod
    def validate_email(cls,value:EmailStr):
        allowed=["apple.in","sony.in"]
        val=str(value).split("@")[-1].lower()
        if val not in allowed:
            raise ValueError("Invalid Email")

        return value
class Product(BaseModel):
    id: UUID
    sku: Annotated[str,Field(min_length=3,max_length=50,description="SKU of product/device",examples=["abc-def-000"])]
    name: Annotated[str,Field(min_length=1,max_length=50,title="Name",description="Product name",examples=["Product name"])]
    category: Annotated[str,Field(description="Category of product/device")]
    price: Annotated[int,Field(gt=0, description="Price of product/device")]
    currency: Literal["INR"] = "INR"
    stock: Annotated[int,Field(ge=0, description="Stock of product/device")]
    rating: Annotated[float,Field(ge=0, le=5, description="Rating of product/device")]
    brand: Annotated[str,Field(min_length=1, max_length=50, description="Brand name")]
    description: Annotated[str,Field(min_length=1, max_length=200, description="Product description")]
    is_available: bool
    seller:Seller
    dimensions:Dimension
    created_at: datetime = Field(default_factory=datetime.utcnow)

#field validator only works on single field
    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku(cls,value:str):
        if "-" not in value:
            raise ValueError("Invalid SKU")
        last=value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("Invalid SKU must end with 3-digit number")

        return value

#use model validator for validating multiple fields, we use the entire pydantic class as input and validate fields
#here we check if the stock of a product is 0 we will not accept it is an input
    @model_validator(mode="after")
    @classmethod
    def validater(cls,model:"Product"):
        if model.stock==0 and model.is_available:
            raise ValueError("if stock is 0 , model should not be available")

        return model
#computed field is used to create a new field using 2 or more original fields, perform operation on
# original field for output as a new field
# the new field will be seen at the end of the file
    @computed_field
    @property
    def final_price(self)->float:
        return self.price-10000

    @computed_field
    @property
    def volume(self)->float:
        return self.dimensions.length*self.dimensions.width*self.dimensions.height