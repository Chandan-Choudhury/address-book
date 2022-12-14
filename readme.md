# Address Book Backend

<img src="/image/img.png">

## Setup project & run on local machine

`Note : Use 3.8 or 3.9`

#### 1. Clone the repository :

```
git clone https://github.com/Chandan-Choudhury/address-book.git
```

#### 2. Create a virtual environment with the following command :

##### a. For ubuntu/macos

```
python3 -m venv venv
```

##### b. For Windows

```
pip install virtualenv
```

```
virtualenv venv
```

#### 3. Activate the virtual environment :

##### a. For ubuntu/macos

```
source venv/bin/activate
```

##### b. For Windows

```
venv\Scripts\activate
```

#### 4. Install the required libraries :

```
pip install -r requirements.txt
```

#### 5. Run the project on local machine :

```
uvicorn main:app --reload
```

#### 6. Open the browser enter below url to test the API with FastAPI - Swagger UI :

```
http://127.0.0.1:8000/docs
```

or

```
http://localhost:8000/docs
```

## API ENDPOINTS

| Method   | Endpoints                                                 | Description                                                       | Request body                                                 | Path Parameters (datatypes)                          |
| :------- | :-------------------------------------------------------- | :---------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------- |
| `GET`    | `/`                                                       | Fetch all address                                                 | Not Required                                                 | Not Required                                         |
| `GET`    | `/{id}`                                                   | Fetch address by id                                               | Not Required                                                 | `id: int`                                            |
| `GET`    | `/location/{city}`                                        | Fetch address by city name                                        | Not Required                                                 | `city: str`                                          |
| `GET`    | `/coordinates/{longitude}/{latitude}`                     | Fetch addresses by longitude and latitude (Coordinates)           | Not Required                                                 | `longitude: float, latitude: float`                  |
| `GET`    | `/coordinates-distance/{longitude}/{latitude}/{disatnce}` | Fetch nearby addresses by longitude, latitude and distance(in KM) | Not Required                                                 | `longitude: float, latitude: float, distance: float` |
| `POST`   | `/`                                                       | Create a new address                                              | `{"city": "string", "longitude": float, "latitude": float }` | Not Required                                         |
| `PUT`    | `/{id}`                                                   | Update address by id                                              | `{"city": "string", "longitude": float, "latitude": float }` | `id: int`                                            |
| `DELETE` | `/{id}`                                                   | Delete address by id                                              | Not Required                                                 | `id: int`                                            |
