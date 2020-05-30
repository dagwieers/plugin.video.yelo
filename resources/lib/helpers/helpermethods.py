# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from data import PROTOCOLS

CACHE_FILE_NAME = "data.json"


def regex(query, url):
    import re
    try:
        return re.findall(r"%s" % (query), url)[0]
    except IndexError:
        return None


def login_payload(username, password):
    return {
        'j_username': '{}'.format(username),
        'j_password': '{}'.format(password),
        'rememberme': 'true'
    }


def oauth_refresh_token_payload(refresh_token, callback_url):
    import json
    refresh_token_payload = {
        "OAuthTokenParamsRequest":
            {
                "refreshToken": refresh_token,
                "redirectUrl": callback_url
            }
    }

    return json.dumps(refresh_token_payload)


def oauth_payload(auth_token, callback_url):
    import json
    oauth = dict(
        OAuthTokenParamsRequest=dict(
            authToken=auth_token,
            redirectUrl=callback_url,
        ),
    )
    return json.dumps(oauth)


def device_payload():
    import json
    registration = dict(
        deviceRegistration=dict(
            deviceProperties=dict(
                dict=[
                    dict(key='DEVICE_OS', value='Web'),
                    dict(key='OS_NAME', value='Windows'),
                    dict(key='OS_VERSION', value='10'),
                    dict(key='BROWSER_NAME', value='Firefox'),
                    dict(key='BROWSER_VERSION', value='63.0'),
                    dict(key='SCREEN_RESOLUTION', value='1920x1080'),
                    dict(key='SCREEN_DENSITY', value='1'),
                    dict(key='DEVICE_TYPE', value='desktop'),
                ],
            ),
        ),
    )
    return json.dumps(registration)


def stream_payload(device_id, channel_id, protocol=PROTOCOLS.DASH):
    import json
    stream = dict(
        stream=dict(
            protocol=protocol,
            drmMethod='WIDEVINE',
            platform='Web',
            deviceId=device_id,
            context='Watch-TV',
            resource=dict(
                watchMode='Live',
                links=dict(
                    tvChannel=channel_id,
                ),
                timeShiftOffset=0,
            )
        )
    )
    return json.dumps(stream)


def widevine_payload_package(device_id, customer_id):
    import json
    payload = {
        "LatensRegistration": {
            "CustomerName": "{}".format(customer_id),
            "AccountName": "PlayReadyAccount",
            "PortalId": "{}".format(device_id),
            "FriendlyName": "THEOPlayer",
            "DeviceInfo": {
                "FormatVersion": "1",
                "DeviceType": "PC",
                "OSType": "Win32",
                "DRMProvider": "Google",
                "DRMVersion": "1.4.8.86",
                "DRMType": "Widevine",
                "DeviceVendor": "Google Inc.",
                "DeviceModel": ""
            }
        },
        "Payload": "b{SSM}"
    }

    return json.dumps(payload)


def authorization_payload(acces_token):
    return "Bearer {}".format(acces_token)


def is_in_cache(key):
    import json
    import os
    from kodiwrapper import KodiWrapper

    path = KodiWrapper.get_addon_data_path()

    if not os.path.isfile(os.path.join(path, CACHE_FILE_NAME)):
        return False

    with open(os.path.join(path, CACHE_FILE_NAME), "r") as json_file:
        data = json.load(json_file)

    return key in data


def cache_to_file(json_data):
    import json
    import os
    from kodiwrapper import KodiWrapper

    path = KodiWrapper.get_addon_data_path()

    if not os.path.exists(path):
        os.mkdir(path, 0o775)

    data = {}
    if os.path.isfile(os.path.join(path, CACHE_FILE_NAME)):
        with open(os.path.join(path, CACHE_FILE_NAME), "r") as json_file:
            data = json.load(json_file)

    data.update(json_data)

    with open(os.path.join(path, CACHE_FILE_NAME), "w") as json_file:
        json.dump(data, json_file)


def get_from_cache(key):
    import json
    import os
    from kodiwrapper import KodiWrapper

    path = KodiWrapper.get_addon_data_path()

    with open(os.path.join(path, CACHE_FILE_NAME), "r") as json_file:
        data = json.load(json_file)

    return data.get(key)


def create_token(size):
    import uuid
    return str(uuid.uuid4()).replace("-", "")[0:size]


def timestamp_to_datetime(timestamp):
    from datetime import datetime
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")
