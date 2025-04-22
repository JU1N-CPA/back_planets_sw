# back_plantes_sw

# Back Planets SW API Documentation

This document provides a step-by-step guide to set up, run, and test the Back Planets SW API.

Considerations and thoughts:
1. Implement unit tests to check specific cases
2. Implement private views for security (optional giving the nature of the case)
3. Implement docker and docker compuse to orchestrate the database easily and the application and easy scalability and dependency
4. Queue messaging as initial steps to implement microservices
5. CI/CD for easy deployment
6. loggers and error handler properly


Note: These are thoughts to improve and create a robust applications. However, it is essential to analyse the business perspective before implement any of those tools.

IMPORTANT: If you want to run the app using Docker, go to step 7
---

## Table of Contents
1. [Installation](#installation)
2. [Database Setup](#database-setup)
3. [Running the Server](#running-the-server)
4. [Testing the API](#testing-the-api)
5. [SQLite Command Line](#sqlite-command-line)
6. [API Endpoints](#api-endpoints)
7. [Docker](#Docker)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/back_planets_sw.git
   cd back_planets_sw

2. **Create a Virtual Environment**:
    ```python
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install requirements.txt**:
    ```python
        pip install -r requirements.txt

## database-setup

1. **Make migrations**
    ```python
        python manage.py makemigrations
        python manage.py migrate

2. **Create a Superuser (Optional)**
    ``` python
        python manage.py createsuperuser

## running-the-server

1. **Create a Superuser (Optional)**
    ```python
        python manage.py runserver

## testing-the-api
- Install the extension REST Client by Huachao Mao
- Open the file "test.http"
- select the test, right click and click on "Send request"
- See the results
- Alternative: use the restframework to test the endpoints

## sqlite-command-line

1. **Open the SQLite shell**
    ```bash
        sqlite3 db.sqlite3

2. **View Tables**
    ```bash
        .tables

3. **View Schema**
    ```bash
        .schema
4. **Run query**
    ```bash
        SELECT * FROM planets_planet;

5. **Exit SQLite**
    ```bash
        .exit

## api-endpoints

### Available Endpoints
| Method | Endpoint                          | Description                          |
|--------|-----------------------------------|--------------------------------------|
| GET    | `api/Fetchplanets/`                 | Fetch and save planets from an external API |
| GET    | `api/AllPlanets/`                   | Retrieve all planets                 |
| GET    | `api/planetview/<str:name>/`        | Retrieve a specific planet by name   |
| POST   | `api/planets/create/`               | Create a new planet                  |
| DELETE | `api/planets/delete/<str:name>/`    | Delete a specific planet by name     |
| PUT    | `api/planets/update/<str:name>/`    | Update a specific planet by name     |
| POST   | `api/api/register/`                 | Register into the DB to get the auth |
| POST   | `api/api-token-auth/`               | Get the token once register is done  |
| PATCH  | `api/planets/update-partial/`       | modify a planet partially            |
| GET    | `api/planets/`                      | Filter by specific attribute of the planet e.g ?climates__icontains=arid  |


## Explaination
/Fetchplanets/
Method: GET
Description: Fetches planets from an external API and saves them to the database.

/AllPlanets/
Method: GET
Description: Retrieves all planets stored in the database.

/planetview/<str:name>/
Method: GET
Description: Retrieves details of a specific planet by its name.

/planets/create/
Method: POST
Description: Creates a new planet in the database. Requires a JSON payload with planet details.

/planets/delete/<str:name>/
Method: DELETE
Description: Deletes a specific planet from the database by its name.

/planets/update/<str:name>/
Method: PUT
Description: Updates the details of a specific planet by its name. Requires a JSON payload with updated planet details.

/api/register/
Method: POST
Description: Registers a new user. Requires username and password to be stored for future token-based authentication.

/api-token-auth/
Method: POST
Description: Logs in a registered user and returns an authentication token for use in future requests.

/planets/update-partial/
Method: PATCH
Description: Updates only the specified fields of a planet record. Useful for minor changes without affecting other data.

/planets/
Method: GET
Description: Retrieves planets filtered by query parameters like name, population__gte, climates, etc.
Example: /planets/?name=Tatooine&climates__icontains=arid


## 7. Docker

## 🧱 Project Structure
starwars_project/ ├── starwars_project/ # Django project ├── planets/ # Django app ├── manage.py ├── requirements.txt ├── Dockerfile ├── .dockerignore └── docker-compose.yml

---

## ⚙️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### 1. Build & Run the App

    ```bash
        docker-compose up --build

### 2.  Access the Running Container to query the database
    ``` bash
        docker ps  # Find the container name
        docker exec -it starwars_project_web_1 sh  # Or /bin/bash
        ls

### 3.  Access the Running Container to query the database
    ```bash
        .tables
        .schema
        SELECT * FROM planets_planet;
        .quit

### 4.  Stop and restart Docker
    ```bash
        docker-compose down
        docker-compose up
    
### 5.  Full clean
    ```bash
        docker-compose down -v --rmi all


 
