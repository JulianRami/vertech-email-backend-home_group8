# Vertech-Email-Backend

## Environment variables

Inside the root folder, provide a .env file with the following contents:

FLASK_APP=app.app

FLASK_ENV=development || production || testing

JWT_SECRET_KEY="your_secret_jwt_string"

DATABASE_URL=your_database_URI (only needed if FLASK_ENV=production)

## Installing dependencies

From the vertech-email-backend folder:

    python3 -m venv .venv

    . .venv/bin/activate

    pip install -r requirements.txt

## Creating the database tables / Performing migrations

From the vertech-email-backend folder:

    . .venv/bin/activate

    flask db init
    flask db migrate
    flask db upgrade

## Running the project

From the vertech-email-backend folder:

    flask run --debug
  
## Swagger UI Docs

You can go to http://localhost:5000/api/swagger-ui for a full documentation in the [api](https://imgur.com/WJrg1F4)

---

## Improvements

1. Cleaning some functions calling that weren't used in some files
2. Create a docker compose file to run needed services in local
3. The code is documented
