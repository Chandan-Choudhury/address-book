from pydantic import BaseModel

# Create a class that inherits from BaseModel
class Address(BaseModel):
    city:str
    longitude:float
    latitude:float