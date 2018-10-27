from flask import Flask
from flask_cors import CORS

from core import loop
from model.base import BaseModel
from objects import index, register, get_file_status, get_registration
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

# Configure App from environment
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

urls = [
    Route('/', ['GET'], index),
    Route('/request/<string:club_name>/register', ['PUT', 'POST'], register),
    Route('/request/<string:request_id>/', ['GET'], get_file_status),
    Route('/registration/<string:club_name>/<string:year>/<string:user_id>/', ['GET'], get_registration),
    Route('/registration/<string:club_name>/latest/<string:user_id>/', ['GET'], get_registration),
    Route('/registration/', ['GET'], get_registration).has_query_params(
        ("club_name", str, False),
        ("year", str, True),
        ("user_id", str, True),
    ),
]

app.before_first_request(loop)
app.before_first_request(BaseModel.setup)

create_routes(app, urls)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
