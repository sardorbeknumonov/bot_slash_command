import json

from flask import Flask, request

import requests

host = "https://api-88CA8C74-5A5F-4A67-ABCA-C23D24C33C37.sendbird.com/v3"
bot_id = "info_bot"
api_token = "3e4bb5be554433a29fb8cced3a38b74aae39f85f"
app = Flask(__name__)

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


# message event handler which receive a message from sendbird
@app.route('/', methods=['POST'])
def post_request():
    requested_params = request.get_json()
    category = requested_params[REQUEST_CATEGORY]
    channel = requested_params["channel"]
    message = requested_params['message']
    messageText = str(message['text'])
    # check message start with `/`
    if messageText.startswith("/"):
        # split message with space. because user put space after slash command
        splited_text = messageText.split(" ")
        # exract command from splitted text
        command = splited_text.pop(0)
        # run response by command func
        res = response_by_command(command, splited_text, channel)
        if res:
            send_message_to_channel(res, channel['channel_url'])
    elif messageText.__contains__('/'):
        print()
    return HTTP_VALID_RESPONSE


def response_by_command(command, splited_text, channel):
    if command == '/invite_people':
        body = {
            "user_ids": splited_text
        }
        endpoint_invite = host + "/group_channels/" + channel['channel_url'] + "/invite"
        res = request_to_sb(method='POST', endpoint=endpoint_invite, data=body, token=api_token)
        if res and res.status_code == 200:
            peoples = ""
            for i, userId in enumerate(splited_text):
                if i == 0:
                    peoples += userId
                else:
                    peoples += ', ' + userId
            msg = f"{bot_id} invited {peoples} to {channel['name']} channel"
            send_message_to_channel(msg, channel['channel_url'])

    elif command == '/coronavirus':
        req = requests.get("https://api.covid19api.com/summary")
        res = req.json()
        body = f"NewConfirmed{res['Global']['NewConfirmed']}\nTotalConfirmed: {res['Global']['TotalConfirmed']}\nNewDeaths: {res['Global']['NewDeaths']}\nTotalDeaths {res['Global']['TotalDeaths']}"
        return body
    elif command == '/meme':
        endpoint_meme = "https://meme-api.herokuapp.com/gimme/1"
        res = requests.get(endpoint_meme)
        body = res.json()
        message = f"{body['memes'][0]['title']}\n{body['memes'][0]['url']}"
        return message
    elif command == '/who_is':
        userId = splited_text[0]
        endpoint_user = f"{host}/users/{userId}"
        res = request_to_sb('GET', endpoint_user, token=api_token)
        message = ""
        if res.status_code == 200:
            body = res.json()
            metadata = body['metadata']
            mdata = ""
            for key, value in metadata.items():
                mdata += f"\n{key}:{value}"

            if userId == bot_id:
                message = f"This is me! 😎 "
            else:
                message = f"Nickname of {userId} is {body['nickname']}.{mdata}"
        elif res.status_code == 400:
            message = "User not founded"
        return message
    elif command == '/show_members':
        endpoint_channel = f"{host}/group_channels/{channel['channel_url']}/members"
        res = request_to_sb('GET', endpoint_channel, token=api_token)
        if res.status_code == 200:
            body = res.json()
            members = body['members']
            message = ""
            for i, member in enumerate(members):
                if i == 0:
                    message += f"{member['user_id']} -- {member['nickname']}"
                else:
                    message += f"\n{member['user_id']} -- {member['nickname']}"
            return message
        else:
            message = "Members not found"
            return message
    else:
        message = f"Sorry, I don't have {command} command yet!"
        return message


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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
