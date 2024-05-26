
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
class Product(BaseModel):
    name: str = Field(description="Name of the product")
    link: str = Field(description="Link to buy the product")
    price: str = Field(description="Price of the product")
    website: str = Field(description="Website where the product was found")

class Products(BaseModel):
    products: List[Product]
