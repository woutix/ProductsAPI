from pydantic import BaseModel


class Config: # TODO: сделать что-нибудь позже
   from_attributes = True
      
class ProductAddSchema(BaseModel):
   name: str
   price: int
   amount: int
    
class ProductSchema(ProductAddSchema):
   id: str

class ProductIdSchema(BaseModel):
   product_id: int 

class ProductResponseSchema(BaseModel):
    id: str 
    name: str
    price: int
    amount: int

    @property
    def id(self) -> str:
        return str(self._id)
    
    # Переопределим конструктор
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id = kwargs.get('id') 
