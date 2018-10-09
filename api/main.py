from flask import Flask
from flask_cors import CORS

from modules.objects import index
from utilities.router import create_routes, Route

app = Flask(__name__)
CORS(app)

urls = [
    Route('/', ['GET'], index).has_query_params(
        ('test', str, False)
    ),
    # Route('/index', ['GET'], index)
]

create_routes(app, urls)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)
