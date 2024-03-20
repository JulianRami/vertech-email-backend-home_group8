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

## Improvements - Milestone 2: Maturing - backend

As code improvements for back-end from group 9 to group 8, we suggest:

1. Cleaning some functions calling that weren't used in some files
2. Create a docker compose file to run needed services in local, which facilite running the project on any machine (simulating production enviroment). With this, when run `docker compose up` you only have an .env file like:

        FLASK_APP=app.app
        FLASK_ENV=production
        DATABASE_URL=postgresql://postgres:your_password@db:5432/your_database
        JWT_SECRET_KEY=your_secret_jwt_string

3. The code is documented
4. The Schemas are ordered by categories
5. The Dockerfile includes documentation that outlines the proposed steps for the build process.
6. Environment variables from the .env file are not set inside the build recipe. This helps to ensure the adequate management of environment variables.
7. Implements testing pipeline with informative summary, in order to find and address bugs quicker. You can check informative test results in Summary tab of ci workflow in Github.

Preview suggestions are related to the pull request: 

1. [Docker improvement adn folder schemas](https://github.com/TechFellowGroup8/vertech-email-backend/pull/19#issue-2198402815)
2. [CI testing improvement and function docs](https://github.com/TechFellowGroup8/vertech-email-backend/pull/20#issue-2198464152)