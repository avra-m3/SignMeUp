import os

from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate

import controllers
from model.database import db
from utilities import security
from utilities.core import EnvVariable, extract_environment_to_flask
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

environment = [
    # Application variables
    EnvVariable("GCLOUD_BUCKET", required=True),
    EnvVariable("GOOGLE_APPLICATION_CREDENTIALS", required=True),

    # Important Flask inbuilt variables
    EnvVariable("DEBUG", default=False),
    EnvVariable("SECRET_KEY", required=True),

    # SQL Alchemy (Database/ORM) variables
    EnvVariable("SECURITY_PASSWORD_HASH", default="bcrypt"),
    EnvVariable("SECURITY_PASSWORD_SALT", default=os.getenv("SECRET_KEY")),
    EnvVariable("SQLALCHEMY_TRACK_MODIFICATIONS", default=False),
    EnvVariable("DATABASE_URI", required=True, map_to="SQLALCHEMY_DATABASE_URI"),

    # Flask inbuilt variables
    EnvVariable("SERVER_NAME"),
    EnvVariable("APPLICATION_ROOT"),
    EnvVariable("PREFERRED_URL_SCHEME"),
    EnvVariable("JSON_SORT_KEYS"),
    EnvVariable("MAX_CONTENT_LENGTH", default=16 * 1024 * 1024),
]


urls = [
    Route('/', ['GET'], controllers.index),
    Route('/authorize', ['GET'], controllers.authorize),
    Route('/club', ['GET'], controllers.get_clubs),
    Route('/club/<string:club_name>/register', ['PUT', 'POST'], controllers.register),
    Route("/club/<string:club_name>/register/<string:student_id>", ['GET'], controllers.get_registration_by_details),
    Route('/registration/<string:registration_id>', ['GET'], controllers.get_registration),

    Route("/user", ["PUT", "POST"], controllers.create_user).has_args(
        ("email", str, False),
        ("password", str, False),
    ),

    Route("/user/<string:email>", ["GET"], controllers.get_user),

    Route("/student/<string:student_id>", ["UPDATE", "PUT"], controllers.update_user_by_student_id).has_args(
        ("first_name", str, False),
        ("last_name", str, False),
        ("email", str, False),
    ),
]

create_routes(app, urls)
extract_environment_to_flask(app, environment)

with app.app_context():
    print("Creating Database")
    db.init_app(app)
    print("Running Migrations...")
    Migrate(app, db)
    print("Running Creates...")
    db.create_all()
    print("Database Commit...")
    db.session.commit()
    print("Security Setup...")
    security.setup(app)
    print("Ready!")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
