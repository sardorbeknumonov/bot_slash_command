from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def get_request():
    return "Hello World!"


@app.route('/', methods=['POST'])
def post_request():
    requested_params = request.get_json()

    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
