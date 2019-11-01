"""订阅"""

import json

from tap_tools import _process_value, subscibe_topics

request_params = {
    "type": "sub",
    "topics": ['LME-F-CA-3M', 'HKEX-F-MHI-1911', 'NYMEX-F-CL-2004'],
}


def my_on_message(ws, message):
    msg = json.loads(message)
    for key, value in msg.items():
        msg[key] = _process_value(key, value)
    print(msg)


subscibe_topics(request_params, my_on_message)
