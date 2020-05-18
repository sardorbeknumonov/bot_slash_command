from flask import Flask
from route import api

application = Flask(__name__)
application.debug = True

application.register_blueprint(api)
if __name__ == '__main__':
    try:
        application.run(host='0.0.0.0')
    except IndexError:
        print('Wrong run command.\n')
        print('python app.py <API_HOST> <APP_TOKEN> <BOT_ID>')
