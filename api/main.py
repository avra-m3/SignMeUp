from flask import Flask
from flask_cors import CORS

from model.base import BaseModel
from objects import index, register, get_file_status, get_registration
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

# Configure App from environment
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

urls = [
    Route('/', ['GET'], index),
    Route('/club/<string:club_name>/registration', ['PUT', 'POST'], register),
    Route('/club/<string:club_name>/registration/<string:request_id>/', ['GET'], get_file_status),
    Route('/club/<string:club_name>/<string:year>/<string:user_id>/', ['GET'], get_registration),
]

create_routes(app, urls)
BaseModel.setup()

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
