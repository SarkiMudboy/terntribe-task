## TERNTRIBE TASK

## Description

A RESTful API to manage social causes and user contributions.

## Stack

- API -> Django REST Framework.
- DB -> Postgres/SQLite.

## Config

The project depends on an `.env` file which is loaded at runtime. The .env file should live in the root directory and contain the following variables.

```
SECRET_KEY=(a secret string of characters)
DEBUG=(bool)
USE_POSTGRES=(bool)

// for postgres

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

## Usage

Install Python

Setup and install python, see [Setup Python](https://www.python.org/downloads/)

_(This project assumes Python 3.11.3)_

Clone the repo using

```
git clone https://github.com/SarkiMudboy/terntribe-task.git
```

Install dependencies using `pip`, including any optional packages you want...

```
pip install -r requirements.txt
```

Run migrations

```
python manage.py makemigrations
python manage.py maigrate
```

Start the development server `python manage.py runserver`

Visit homepage `http://localhost:8000`

## Tests

All tests live in causes/tests.py.

Run tests using

```
python manage.py test
```

To run a specific test use `python manage.py test causes.tests.TestClass.testname`

## Schema and Browsable API

The app uses `drf-spectacular` to include interactive and up-to-date documentation and also provides a Swagger UI.

Run the server using

```
python manage.py runserver
```

and visit `http://localhost:8000/api/v1/schema` to obtain a `yml` file of the API schema.

To use Swagger UI, visit `http://localhost:8000/api/v1/` or `http://localhost:8000/api/v1/schema/redoc`
