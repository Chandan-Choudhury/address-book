"""
This is the main python module of this project.
"""

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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

# Origin URLS list
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://chandanchoudhury.in",
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is a decorator that tells FastAPI that this function is a path operation
@app.get("/")
# This is a path operation function to get all addresses from DB
def get_addressess(session: Session = Depends(get_session)):
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
def get_address_by_id(id:int, session: Session = Depends(get_session)):
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


@app.get("/location/{city}")
# This is a path operation function to get a specific address from DB by city name
def get_address_by_city(city:str, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by city name
        address_by_city = session.query(models.Address).filter(models.Address.city == city).all()
        # Log the address to the console
        print("Address by city : ",address_by_city)
        # Check if there is an address with the given city name in the DB
        if address_by_city == []:
            # If there is no address with the given city name in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found with the given city name."})
        else:
            # If there is an address with the given city name in the DB, return a JSON response with status code 200 and the address
            return address_by_city
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.get("/coordinates/{longitude}/{latitude}")
# This is a path operation function to get a specific address from DB by longitude and latitude
def get_addressess_by_coordinates(longitude:float, latitude:float, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by longitude and latitude
        addresses_by_coordinates = session.query(models.Address).filter(models.Address.longitude == longitude, models.Address.latitude == latitude).all()
        # Log the addresses to the console
        print("Addresses by coordinates : ",addresses_by_coordinates)
        # Check if there are any addresses with the given longitude and latitude in the DB
        if addresses_by_coordinates == []:
            # If there are no addresses with the given longitude and latitude in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found for the given location."})
        else:
            # If there are addresses with the given longitude and latitude in the DB, return a JSON response with status code 200 and the addresses
            return addresses_by_coordinates
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.get("/coordinates-distance/{longitude}/{latitude}/{distance}")
# This is a path operation function to get a specific address from DB by longitude and latitude and distance(in KM)
# Here user need to share his logituude and latitude and a distance value in KM to check if there are any addresses in the given distance from his location
def get_addressess_by_coordinates_and_distance(longitude:float, latitude:float, distance:float, session: Session = Depends(get_session)):
    try:
        # Convert the distance from KM to degrees (Let's take 1 degree = 111 KM as reference here)
        distance_in_degree = distance / 111
        # Log the distance in degrees to the console
        print("Latitude/Logitude distance in degrees :", distance_in_degree)
        # Query the addresses from DB by longitude and latitude and distance
        addresses_by_coordinates_and_distance = session.query(models.Address).filter(models.Address.longitude.between(longitude-distance_in_degree, longitude+distance_in_degree), models.Address.latitude.between(latitude-distance_in_degree, latitude+distance_in_degree)).all()
        # Check if there are any addresses with the given longitude and latitude and distance in the DB
        if addresses_by_coordinates_and_distance == []:
            # If there are no addresses with the given longitude and latitude and distance in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No nearby addresses found for the given location and distance."})
        else:
            # If there are addresses with the given longitude and latitude and distance in the DB, return a JSON response with status code 200 and the addresses
            return addresses_by_coordinates_and_distance
    except:
        # If there is an error, return a JSON response with status code 500 and a message
        return JSONResponse(status_code=500, content={"message": "Something went wrong."})


@app.post("/")
# This is a path operation function to add a new address to DB
def add_address(address: schemas.Address, session: Session = Depends(get_session)):
    try:
        # Create a new address object
        new_address = models.Address(city = address.city.strip(), longitude = round(address.longitude, 6), latitude = round(address.latitude,6))
        # Log the new address to the console
        print("City name :",new_address.city)
        print("Longitude :",new_address.longitude)
        print("Latitude :",new_address.latitude)
        # Add the new address to the DB if below conditions are satisfied
        if new_address.city == "":
            print("City name is empty")
            return JSONResponse(status_code=400, content={"message": "City name is required."})
        elif not -180 <= new_address.longitude <= 180 or new_address.longitude == "":
            print("Longitude is not valid")
            return JSONResponse(status_code=400, content={"message": "Please enter valid Longitude."})
        elif not -90 <= new_address.latitude <= 90 or new_address.latitude == "":
            print("Latitude is not valid")
            return JSONResponse(status_code=400, content={"message": "Please enter valid Latitude."})
        else:
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
def update_address(id:int, address: schemas.Address, session: Session = Depends(get_session)):
    try:
        # Query the address from DB by ID
        address_by_id = session.query(models.Address).get(id)
        # Log the address to the console
        print("Address by id : ",address_by_id)
        # Check if there is an address with the given ID in the DB
        if address_by_id == None:
            # If there is no address with the given ID in the DB, return a JSON response with status code 404 and a message
            return JSONResponse(status_code=404, content={"message": "No address found with the given id to update."})
        # Update the address in the DB if below conditions are satisfied
        elif address.city == "":
            print("City name is empty")
            return JSONResponse(status_code=400, content={"message": "City name is required."})
        elif not -180 <= address.longitude <= 180 or address_by_id.longitude == "":
            print("Longitude is not valid")
            return JSONResponse(status_code=400, content={"message": "Please enter valid Longitude."})
        elif not -90 <= address.latitude <= 90 or address_by_id.latitude == "":
            print("Latitude is not valid")
            return JSONResponse(status_code=400, content={"message": "Please enter valid Latitude."})
        else:
            # If there is an address with the given ID in the DB and above conditions are satisfied, update the address with the new values
            address_by_id.city = address.city.strip()
            address_by_id.longitude = round(address.longitude, 6)
            address_by_id.latitude = round(address.latitude, 6)
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
def delete_address(id:int, session: Session = Depends(get_session)):
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