from flask import Flask
from flask_cors import CORS

from modules.objects import index, register, PATHS
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "./cards"

urls = [
    Route('/', ['GET'], index),
    Route('/register', ['PUT', 'POST'], register)
]

PATHS.create_dirs()
create_routes(app, urls)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
