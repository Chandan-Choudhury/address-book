"""
This is the main python module of this project.
"""

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# Create database tables
Base.metadata.create_all(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Created app object using the FastAPI class
app = FastAPI()


# This is a decorator that tells FastAPI that this function is a path operation
@app.get("/")
# This is a path operation function to get all addresses from DB
def getAddressess(session: Session = Depends(get_session)):
    try:
        # Query all addresses from DB
        addresses = session.query(models.Address).all()
        # Log the addresses to the console
        print("Addresses : ",addresses)
        # Check if there are any addresses in the DB
        if addresses == []:
            # If there are no addresses in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "DB is empty."})
        else:
            # If there are addresses in the DB, return a JSON response with status code 200 and the addresses
            return addresses
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.get("/{id}")
# This is a path operation function to get a specific address from DB by ID(Unique)
def getAddress(id:int, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by ID
        address_by_id = session.query(models.Address).get(id)
        # Log the address to the console
        print("Address by id : ",address_by_id)
        # Check if there is an address with the given ID in the DB
        if address_by_id == None:
            # If there is no address with the given ID in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found with the given id."})
        else:
            # If there is an address with the given ID in the DB, return a JSON response with status code 200 and the address
            return address_by_id
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.get("/{longitude}/{latitude}")
# This is a path operation function to get a specific address from DB by longitude and latitude
def getAddressessByLocation(longitude:float, latitude:float, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by longitude and latitude
        addresses_by_location = session.query(models.Address).filter(models.Address.longitude == longitude, models.Address.latitude == latitude).all()
        # Log the addresses to the console
        print("Addresses by location : ",addresses_by_location)
        # Check if there are any addresses with the given longitude and latitude in the DB
        if addresses_by_location == []:
            # If there are no addresses with the given longitude and latitude in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found for the given location."})
        else:
            # If there are addresses with the given longitude and latitude in the DB, return a JSON response with status code 200 and the addresses
            return addresses_by_location
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.get("/{longitude}/{latitude}/{radius}")
# This is a path operation function to get a specific address from DB by longitude and latitude and radius(in KM)
# Here user need to share his logituude and latitude and a radius value in KM to check if there are any addresses in the given radius from his location
def getAddressessByLocationAndRadius(longitude:float, latitude:float, radius:float, session: Session = Depends(get_session)):
    try:
        # Convert the radius from KM to degrees (Let's take 1 degree = 111 KM as reference here)
        radius_in_degree = radius / 111
        # Log the radius in degrees to the console
        print("Latitude/Logitude radius in degrees :", radius_in_degree)
        # Query the addresses from DB by longitude and latitude and radius
        addresses_by_location_and_radius = session.query(models.Address).filter(models.Address.longitude.between(longitude-radius_in_degree, longitude+radius_in_degree), models.Address.latitude.between(latitude-radius_in_degree, latitude+radius_in_degree)).all()
        # Check if there are any addresses with the given longitude and latitude and radius in the DB
        if addresses_by_location_and_radius == []:
            # If there are no addresses with the given longitude and latitude and radius in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found for the given location and radius."})
        else:
            # If there are addresses with the given longitude and latitude and radius in the DB, return a JSON response with status code 200 and the addresses
            return addresses_by_location_and_radius
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.post("/")
# This is a path operation function to add a new address to DB
def addAddress(address: schemas.Address, session: Session = Depends(get_session)):
    try:
        # Create a new address object
        new_address = models.Address(city = address.city, longitude = address.longitude, latitude = address.latitude)
        # Log the new address to the console
        print("addr",new_address.city)
        # Add the new address to the DB
        session.add(new_address)
        # Commit the changes to the DB
        session.commit()
        # Refresh the session
        session.refresh(new_address)
        # Return a JSON response with status code 201 and the new address
        return JSONResponse(status_code=201, content={"message": "Address added successfully."})
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.put("/{id}")
# This is a path operation function to update an existing address in DB by ID(Unique)
def updateAddress(id:int, address: schemas.Address, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by ID
        address_by_id = session.query(models.Address).get(id)
        # Log the address to the console
        print("Address by id : ",address_by_id)
        # Check if there is an address with the given ID in the DB
        if address_by_id == None:
            # If there is no address with the given ID in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found with the given id to update."})
        else:
            # If there is an address with the given ID in the DB, update the address with the new values
            address_by_id.city = address.city
            address_by_id.longitude = address.longitude
            address_by_id.latitude = address.latitude
            # Commit the changes to the DB
            session.commit()
            # Refresh the session
            session.refresh(address_by_id)
            # Return a JSON response with status code 200 and the updated address
            return JSONResponse(status_code=200, content={"message": "Address updated successfully."})
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.delete("/{id}")
# This is a path operation function to delete an existing address from DB by ID(Unique)
def deleteAddress(id:int, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by ID
        address_by_id = session.query(models.Address).get(id)
        # Log the address to the console
        print("Address by id : ",address_by_id)
        # Check if there is an address with the given ID in the DB
        if address_by_id == None:
            # If there is no address with the given ID in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found with the given id to delete."})
        else:
            # If there is an address with the given ID in the DB, delete the address
            session.delete(address_by_id)
            # Commit the changes to the DB
            session.commit()
            # Close the session
            session.close()
            # Return a JSON response with status code 200 and a message
            return JSONResponse(status_code=200, content={"message": "Address deleted successfully."})
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})