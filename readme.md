# Address Book Backend

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
