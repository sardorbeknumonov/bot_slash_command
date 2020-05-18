import json

import requests

from config import api_token, host, bot_id


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
        return res

    elif method == 'GET':
        res = requests.get(endpoint, headers=headers)
        return res
    else:
        raise ValueError('Request method must be POST, GET , DELETE or PUT')


ENDPOINT_BOT = host + '/bots/{}'.format(bot_id)
ENDPOINT_SEND_MESSAGE = ENDPOINT_BOT + '/send'
