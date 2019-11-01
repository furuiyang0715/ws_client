import json
import logging
import time
from functools import partial

import websocket

try:
    import thread
except ImportError:
    import _thread as thread

logger = logging.getLogger()


def _on_message(ws, message):
    pass


def _on_error(ws, error):
    pass


def _on_close(ws):

    pass


def _on_open(ws, **kwargs):
    def run(kwargs):
        msg = json.dumps(kwargs['kwargs'])
        ws.send(msg)

    # TODO 客户端的单线程启动和多线程启动
    # run(kwargs)

    thread.start_new_thread(run, (kwargs,))


def _process_value(field, value):
    """数据类型处理
    """
    str_fields = [
        "exchangeno",
        "commoditytype",
        "commodityno",
        "contractno",
    ]

    repeated_fields = [
        "qbidprice",
        "qbidqty",
        "qaskprice",
        "qaskqty",
    ]

    float_fields = [
        "qpreclosingprice",
        "qlastprice",
        "qopeningprice",
        "qhighprice",
        "qlowprice",
        "qhishighprice",
        "qhislowprice",
        "qlimitupprice",
        "qlimitdownprice",
        "qtotalqty",
        "qtotalturnover",
        "qpositionqty",
        "qaverageprice",
        "qclosingprice",
        "qsettleprice",
        "qlastqty",
        "qimpliedbidprice",
        "qimpliedbidqty",
        "qimpliedaskprice",
        "qimpliedaskqty",
        "qpredelta",
        "qcurrdelta",
        "qinsideqty",
        "qoutsideqty",
        "qturnoverrate",
        "q5davgqty",
        "qperatio",
        "qtotalvalue",
        "qnegotiablevalue",
        "qpositiontrend",
        "qchangespeed",
        "qchangerate",
        "qchangevalue",
        "qswing",
        "qtotalbidqty",
        "qtotalaskqty",
        ""
    ]
    if field == "ts":
        pass
    elif field in str_fields:
        value = str(value)
    elif field in float_fields:
        value = float(value)
    elif field in repeated_fields:
        lst = value.strip("/").split("/")
        value = [float(v) for v in lst]
    else:
        pass
    return value


class Reports(object):
    def __init__(self, params: dict, on_message=_on_message, on_error=_on_error):
        self.client_run(params=params, on_message=on_message, on_error=on_error)

    def client_run(self, url='ws://tap-api.jingzhuan.cn:46399/',
    # def client_run(self, url='ws://127.0.0.1:46399/',
                   on_message=_on_message,
                   on_error=_on_error,
                   on_close=_on_close,
                   on_open=_on_open,
                   debug=False,
                   params={}):
        websocket.enableTrace(debug)
        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        on_open = partial(on_open, kwargs=params)
        ws.on_open = on_open
        ws.run_forever()


def get_exists_topics():
    msg = None
    request_params = {"type": "get", "method": "exists_topics"}

    def on_message(ws, message):
        nonlocal msg
        msg = json.loads(message)

    Reports(params=request_params, on_message=on_message)
    return msg


def get_active_topics():
    msg = None
    request_params = {"type": "get", "method": "active_topics"}

    def on_message(ws, message):
        nonlocal msg
        msg = json.loads(message)

    Reports(params=request_params, on_message=on_message)
    return msg


def get_history_datas(request_params):

    lst = []

    def on_msg(ws, message):
        msg = json.loads(message)
        lst.append(msg)

    Reports(params=request_params, on_message=on_msg)
    processed_lst = []

    for report in lst:
        for key, value in report.items():
            report[key] = _process_value(key, value)
        processed_lst.append(report)

    return processed_lst


def subscibe_topics(request_params, on_message):
    retry = []

    def my_on_error(ws, error):
        retry.append(ws)

        while len(retry) < 10:
            logger.warning(f"第{len(retry)}次失败重试中")
            time.sleep(3)
            Reports(params=request_params, on_message=on_message, on_error=my_on_error)
            return
        logger.warning("服务异常 请咨询管理员")

    Reports(params=request_params, on_message=on_message, on_error=my_on_error)
