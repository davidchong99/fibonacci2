# Fibonacci Sequence API
This API will return the Fibonacci sequence starting from 0 up to the number provided by the users. 
The catch is the numbers in a Fibonacci sequence can be extremely large that they exceed the maximum number allowed in the database or operating system.
For postgres database, I choose the type numeric to store largest possible number allowed in postgres.

Its implementation details are as follows:

* Python
* FastAPI framework
* Docker
* Postgres database
* SQLModel as database ORM

# Compilation
To compile and run this API locally, Python and Docker should be installed on your PC.
Please follow the steps below:
```console
sudo apt install build-essential python3-dev libpq-dev -y
cd fibonacci
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
docker compose up --build
```
To kill the server, press ctrl + c on the keyboard.

## API Usage Guide
This API has 4 functionalities or endpoints. The following show a sample usage.
1. To get Fibonacci sequence up to 100: 
```console
curl -X GET localhost:8080/100 -H 'Content-Type: application/json'
```
The response returned is as below:
```console
{"sequence":[0,1,1,2,3,5,8,13,34,55,89]}
```
2. To get the Fibonacci sequence with pagination (page_number=0):
```console
curl -X GET localhost:8080/100000/paged?page_number=0 -H 'Content-Type: application/json'
```
The first page always starts with 0.
The response returned is as follows:
```console
{"page_number":0,"total_pages":1,"sequence":[0,1,1,2,3,5,8,13,34,55,89,144,233,377,610,987,1597,2584,4181,6765,10946,17711,28657,46368,75025]}
```
3. To blacklist a number, i.e. 21, and hide it from being shown in Fibonacci sequence:
```console
curl -X POST localhost:8080/blacklist -H 'Content-Type: application/json' -d '{"black_list": 21}'
```
The API will return the existing list of blacklisted numbers:
```console
{"blacklists":[21]}
```
4. To remove an existing blacklisted number:
```console
curl -X DELETE localhost:8080/blacklist/21 -H 'Content-Type: application/json'
```
The API will return status 204 without any response object

## Architecture
All source codes are in /app directory.

main.py serves as the main entry point of this API.

_app_lifespan function is run before the start of the API to create the tables defined in /app/database/models.py

There is only one router defined in /app/fibonacci_router/fibonacci.py where all the endpoints of this router is defined.

The business logic of the endpoints is defined in /app/fibonacci_router/service.py

The data transfer objects are defined in /app/fibonacci_router/dto.py

All database manager related codes are found in /app/database

## Tests
End-to-end tests are found in tests/e2e_tests. 

The run_tests.sh script will set up the env before running all tests with pytest.
