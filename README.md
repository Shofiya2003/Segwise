# Segwise-Service

Test Username and Password:
**Username** : shofiya
**Password**: shofiya

## Quick Start

- If you have docker and docker-compose installed, it's as quick as

```sh
$ cd service
$ docker compose up -d
# or if on an older docker compose
$ docker-compose up -d
```

> **Note**: Make sure to setup the `.env` file first so that the app can connect to the required data

For more details check [set up env variables](#env)

## Manual Setup

If working with a raw system without docker or any other container services, you can setup the project using a very basic python 3 setup.

The following steps should help with getting it all up and running.

- Clone this repository
- Create python virtual environment

  ```
  python3 -m venv venv
  ```
- ```
  cd service
  ```
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Run the flask app
  ```
  python -m src.app
  ```
- Run celery worker
  ```
  celery -A worker worker --loglevel=INFO
  ```

## Database and Migrations

- The database will be auto setup using SQLAlchemy due to the low fidelity schema that this app uses. If it ever gets complicated, do make sure to add in and generate migrations using `alembic` and add the migration running process to `./scripts/start.sh` file, which handles running this via docker.

## Setting up .env {#env}

| Environment Variable | Description                            |
|----------------------|----------------------------------------|
| `DB_HOST`       | URL of the SQLite Database  [sqlite:///database/file.db]
| `JWT_SECRET_KEY`            | JWT Secret |
| `BROKER`         | RabbitMQ/Redis URL to serve as broker for celery [amqp://user:pass@host:port]              |
| `SENTRY_URL`          | DSN to setup sentry to log errors in production               |

For more details check
- [Sentry](https://docs.sentry.io/concepts/key-terms/dsn-explainer/)
- [Celery Broker] (https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html)

## Architecture Overview

![image](https://github.com/Shofiya2003/Segwise/assets/86974918/0f33c615-ed98-4bbd-93c0-796a38801ac8)

The app consists of two components: 

1. **App**: This service is the backend of the application and is responsible for handling API calls.

2. **CSV Uploading Service**: This service runs in the background with the help of a message queue. Tasks to upload data to the database using a link are queued via an API. The uploading tasks do not block the backend service, thereby making the application more scalable.

Additionally, the following should be included:
- Using Server-Sent Events or a messaging service to inform the user about the success or failure of the queued uploading tasks.

# API Documentation

## Overview

This document provides an overview of the API endpoints, their functionality, and the expected responses.

---

## Endpoints

### 1. Upload CSV
- **URL:** `/api/upload-_csv`
- **Method:** `POST`
- **Description:** Uploads the CSV data from the link to DB.
- **Header:**
  - **Authorization:** Bearer {access_token}
- **Request Parameters:** None
- **Request Body:**
    - `'csv_url'`: link to the CSV  
- **Response:**
  ```json
  {
    "message": "Uploading Task Queued"
  }
  ```

 - **Examples**:

- Example:1 SUCCESS
- Request
  ```
  curl -X POST 'http://localhost:5000/api/upload_csv' \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "csv_url": "https://docs.google.com/spreadsheets/d/15U387I2MZRGbxBenbOzc0cbm6abjiFonTgO_d8ALL8I/edit?usp=sharing"
  }'

  ```
- Response:
  ```
  {
    "message": "Uploading Task Queued"
  }
  ```

  ### 2. Query 
- **URL:** `/api/games`
- **Method:** `GET`
- **Description:** Retrieves a list of games based on query parameters and supports aggregate functions.
- **Header:**
  - **Authorization:** Bearer {access_token}
- **Request Parameters:** 
  - Query parameters can include any of the columns of the `Game` model for filtering, such as `name`, `releaseDate`, `price`, etc.
  - Supports aggregate functions (`sum`, `max`, `min`, `avg`) on integer or float columns. (aggregate_function = column_name)
  - > **Note**: Filtering results and aggregating results are independent of each other. For instance, if a filter applies name=game and sum=price, it does not result in the sum of only those columns where name=game. Support for such functionality could be implemented in the future.
  - Supports greater than and less than searches for dates
- **Request Body:** None
- **Example Request:**
    ```
    curl  'http://localhost:5000api/games?supportedLanguages=English&releaseDate<2017-10-12&price>5&max=positive' \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
    ```
- **Response:**
  ```json
  {
    "games": [
      {
        name="Game"
        other_fields
      },
      ...
    ],
    "aggregate_results": {
      "max_positive": 60,
    }
  }
  ```

### 3. Register User
- **URL:** `/api/auth/register`
- **Method:** `POST`
- **Description:** Registers a new user.
- **Request Body:**
  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```
 - **Example Request:**
  ```
  curl -X POST http://localhost:5000/api/auth/register -H "Content-Type: application/json" -d '{
  "username": "example_user",
  "password": "example_password"
  }'
  ```

- **Responses:**

1. Status Code: 201 Created

    ```json

    {
      "msg": "User created successfully"
    }
    ```

2. Missing Username or Password: Status Code: 400 Bad Request

```json

{
  "msg": "Missing username or password"
}
```

3. User Already Exists:  Status Code: 400 Bad Request

```json

{
  "msg": "User already exists"
}
```
### 4. Login

- **URL:** `/api/auth/login`
- **Method:** `POST`
- **Description:** Logs in an existing user and returns access and refresh tokens.
- **Request Body:**
  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```
- **Example Request:**
  ```
  curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{
  "username": "example_user",
  "password": "example_password"
  }'
  ```

- **Responses:**
  1.Success: Status Code: 200 OK

```json
  {
    "access_token": "ACCESS_TOKEN",
    "refresh_token": "REFRESH_TOKEN"
  }
```
2. Missing Username or Password: Status Code: 400 Bad Request
```json
{
  "msg": "Missing username or password"
}
```
3. Bad Username or Password: Status Code: 401 Unauthorized
```json

{
  "msg": "Bad username or password"
}
```

### 5.Refresh Token Endpoint

- **URL:** `/api/auth/refresh`
- **Method:** `POST`
- **Description:** Refreshes the access token using the refresh token.
- **Request Headers:**
  - **Authorization:** Bearer {refresh_token}
- **Responses:**
  - **Success:**
    ```json
    {
      "access_token": "NEW_ACCESS_TOKEN"
    }
    ```
    - Status Code: `200 OK`

- **Example Request:**
```shell
curl -X POST http://localhost:5000/api/auth/refresh -H "Authorization: Bearer REFRESH_TOKEN"
```

- **Example Response:**
```json
  {
  "access_token": "NEW_ACCESS_TOKEN"
  }
```

## Tech Used
**API** - Flask
**Worker** - Celery and RabbitMQ
**DB** - SQLites