import requests
from flask import request, Blueprint
import json
from config import host, api_token

from message_function import send_message_to_channel, request_to_sb

api = Blueprint('bot_api', __name__)

REQUEST_CATEGORY = 'category'
CAT_MESSAGE_NOTIFICATION = 'bot_message_notification'
CAT_GROUP_CHANNEL_JOIN = 'bot_event/group_channel:join'
CAT_GROUP_CHANNEL_LEAVE = 'bot_event/group_channel:leave'

PARAM_CHANNEL = 'channel'
PARAM_CHANNEL_URL = 'channel_url'
PARAM_MESSAGE = 'message'
PARAM_MESSAGE_TEXT = 'text'
HTTP_VALID_RESPONSE = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/')
def get_request():
    return "Hello World!"


# message event handler which receive a message from sendbird
@api.route('/', methods=['POST'])
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


def response_by_command(command, splited_text, channel, bot_id=None):
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
        body = f"NewConfirmed: {int(res['Global']['NewConfirmed'])}\nTotalConfirmed: {int(res['Global']['TotalConfirmed'])}\nNewDeaths: {int(res['Global']['NewDeaths'])}\nTotalDeaths {int(res['Global']['TotalDeaths'])}"
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
