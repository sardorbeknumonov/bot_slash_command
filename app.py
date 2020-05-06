import json

from flask import Flask, request
from logger import Logger

app = Flask(__name__)

logger = Logger()


@app.route('/')
def get_request():
    return "Hello World!"


@app.route('/', methods=['POST'])
def post_request():
    requested_params = request.get_json()
    logger.request(json.dumps(requested_params))
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
