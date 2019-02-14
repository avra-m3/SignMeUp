import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

import controllers
from model.database import db
from utilities import security
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)
"""
Guide to environment variables
=====================================
Variable            | Required  | Description
-------------------------------------
DATABASE            | No        | The type of database to use (sqlite | mysql | postgre).
DATABASE_CONFIG     | Sometimes | Required when DATABASE = 'mysql' or 'postgre'
MAX_CONTENT_LENGTH  | No        | Sets the maximum request size that can be sent, defaults to 16 mb
GCLOUD_BUCKET       | No        | Sets the name of the google cloud bucket to place files in

"""

app.config["DEBUG"] = os.getenv("DEBUG") or False

if not app.config["DEBUG"]:
    if "DATABASE_URI" not in os.environ:
        print("WARNING: No Environment variable 'DATABASE_URI' provided, using default")

    if "SECRET_KEY" not in os.environ:
        print("WARNING: Please set a 'SECRET_KEY' environment variable for password hash generation")

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_PASSWORD_SALT'] = "{}_signmeup".format(os.getenv("SECRET_KEY"))

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI") or "sqlite://tmp/signmeup"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["GCLOUD_BUCKET"] = os.getenv("GCLOUD_BUCKET") or "csit-cache"

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

    Route("/user/<string:email>", ["GET"], controllers.get_user)
]

create_routes(app, urls)

with app.app_context():
    print("Initializing App...")
    db.init_app(app)
    print("Running Migrations...")
    Migrate(app, db)
    print("Running Creates...")
    db.create_all()
    print("Database Commit...")
    db.session.commit()
    print("Security Setup...")
    security.setup(app)
    print("Done")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
