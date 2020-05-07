import json

from flask import Flask, request
from logger import Logger

import requests

host = "https://api-88CA8C74-5A5F-4A67-ABCA-C23D24C33C37.sendbird.com/v3"
bot_id = "pong_1_bot"
api_token = "3e4bb5be554433a29fb8cced3a38b74aae39f85f"
app = Flask(__name__)

logger = Logger()
REQUEST_CATEGORY = 'category'
CAT_MESSAGE_NOTIFICATION = 'bot_message_notification'
CAT_GROUP_CHANNEL_JOIN = 'bot_event/group_channel:join'
CAT_GROUP_CHANNEL_LEAVE = 'bot_event/group_channel:leave'

PARAM_CHANNEL = 'channel'
PARAM_CHANNEL_URL = 'channel_url'
PARAM_MESSAGE = 'message'
PARAM_MESSAGE_TEXT = 'text'
HTTP_VALID_RESPONSE = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/')
def get_request():
    return "Hello World!"


@app.route('/', methods=['POST'])
def post_request():
    requested_params = request.get_json()
    logger.request(json.dumps(requested_params))
    category = requested_params[REQUEST_CATEGORY]
    channel = requested_params["channel"]
    message = requested_params['message']
    messageText = str(message['text'])

    if messageText.startswith("/"):
        splited_text = messageText.split(" ")
        command = splited_text[0]
        res = response_by_command(command, splited_text)
        send_message_to_channel(res, channel['channel_url'])
    return HTTP_VALID_RESPONSE


def response_by_command(command, splited_text):
    if command == '/invite_people':
        print(command)
    elif command == '/coronavirus':
        req = requests.get("https://api.covid19api.com/summary")
        res = req.json()
        body = f"NewConfirmed{res['Global']['NewConfirmed']}\nTotalConfirmed: {res['Global']['TotalConfirmed']}\nNewDeaths: {res['Global']['NewDeaths']}\nTotalDeaths {res['Global']['TotalDeaths']}"
        return body


def send_message_to_channel(message, channel_url):
    """
    Send message to a certain channel.
    :param message: message content
    :param channel_url: url of channel to send
    """
    request_to_sb(method='POST', endpoint=ENDPOINT_SEND_MESSAGE,
                  data={'channel_url': channel_url, 'message': message}, token=api_token)


def request_to_sb(method, endpoint, data={}, token=None):
    """
    Request to SendBird.
    :param method: method of the request
    :param endpoint: endpoint of the request
    :param data: data to put in the request
    :param token: token to add in the request
    """

    headers = {'Content-Type': 'application/json', 'Api-Token': token}

    if method == 'POST':
        res = requests.post(
            url=endpoint,
            data=json.dumps(data),
            headers=headers
        )
    else:
        raise ValueError('Request method must be POST, GET , DELETE or PUT')


ENDPOINT_BOT = host + '/bots/{}'.format(bot_id)
ENDPOINT_SEND_MESSAGE = ENDPOINT_BOT + '/send'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
