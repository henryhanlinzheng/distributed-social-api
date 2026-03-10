# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

import json
from collections import namedtuple


# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it
    to a DataTuple object.
    '''
    try:
        json_obj = json.loads(json_msg)
        resp_type = json_obj['response']['type']
        resp_msg = json_obj['response']['message']
        resp_token = json_obj['response'].get('token', '')
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple('error', 'invalid JSON', '')

    return DataTuple(resp_type, resp_msg, resp_token)


def join_msg(username: str, password: str) -> str:
    '''
    Create a json string for a join message using the provided
    username and password.
    '''
    msg_dict = {
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    }
    return json.dumps(msg_dict)


def post_msg(token: str, message: str, timestamp: float) -> str:
    '''
    Create a json string for a post message using the provided
    token and message.
    '''
    msg_dict = {
        "token": token,
        "post": {
            "entry": message,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(msg_dict)


def bio_msg(token: str, bio: str, timestamp: float) -> str:
    '''
    Create a json string for a bio message using the provided token and bio.
    '''
    msg_dict = {
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(msg_dict)
