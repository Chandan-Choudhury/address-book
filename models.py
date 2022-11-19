from sqlalchemy import Column, Integer, String, Float
from database import Base 

# Create a class for the Address table
class Address(Base):
    __tablename__ = 'address_book'
    id = Column(Integer, primary_key=True)
    city = Column(String(256))
    longitude = Column(Float)
    latitude = Column(Float)