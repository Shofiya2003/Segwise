# Segwise

## Quick Start

- If you have docker and docker-compose installed, it's as quick as

```sh
$ docker compose up -d
# or if on an older docker compose
$ docker-compose up -d
```

> **Note**: Make sure to setup the `.env` file first so that the app can connect to the required data

For more details check [docker section](#docker)

## Manual Setup

If working with a raw system without docker or any other container services, you can setup the project using a very basic python 3 setup.

The following steps should help with getting it all up and running.

- Clone this repository
- Create python virtual environment

  ```
  python3 -m venv venv
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

## Setting up .env

- DB_HOST [Path to SQLite DB]
- JWT_SECRET_KEY [jwt secret]
- BROKER [RabbitMQ Broker for Celert]

## Docker

TBD
