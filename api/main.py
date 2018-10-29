import json
import os
from flask import Flask
from flask_cors import CORS

from model import BaseModel, SQLITE
from objects import index, register, get_registration
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

# Configure App from environment
app.config["DATABASE"] = os.getenv("DATABASE") or SQLITE
app.config["DATABASE_CONFIG"] = json.loads(os.getenv("DATABASE_CONFIG") or '{}')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

urls = [
    Route('/', ['GET'], index),
    Route('/register/<string:club_name>/', ['PUT', 'POST'], register),
    Route('/registration/<string:registration_id>/', ['GET'], get_registration)
]

BaseModel.setup({
    "DATABASE": app.config["DATABASE"],
    "DATABASE_CONFIG": app.config["DATABASE_CONFIG"],
    "FLASK_APP": app,
})


create_routes(app, urls)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
