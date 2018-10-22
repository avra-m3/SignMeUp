import os
from threading import Thread

from flask import Flask
from flask_cors import CORS

import providers
from modules.objects import index, register, get_file_status
from modules.observer.observer import watch
from modules.path_constants import PATHS
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

# Configure App from environment
app.config["PROVIDER"] = os.getenv("PROC_PROVIDER") or "DB_LOCAL"
app.config["PROC_ROOT"] = os.getenv("PROC_ROOT") or "/process"

if app.config["PROVIDER"] == "DB_REMOTE":
    app.config["DB_HOST"] = os.getenv("ENDPOINT")
    app.config["DB_USER"] = os.getenv("USER")
    app.config["DB_PWD"] = os.getenv("PASSWORD")
    app.config["DB_NAME"] = os.getenv("DATABASE")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

urls = [
    Route('/', ['GET'], index),
    Route('/club/<string:club_name>/registration', ['PUT', 'POST'], register),
    Route('/club/<string:club_name>/registration/<string:card_id>/', ['GET'], get_file_status),
]


@app.before_first_request
def before_first_request():
    """
    Actions to perform before the first request
    :return:
    """
    # Setup the provider before anything else.
    providers.setup(app)
    # Check processing directories exist
    PATHS.create_dirs()
    # Start the observer
    Thread(target=watch).start()


create_routes(app, urls)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
