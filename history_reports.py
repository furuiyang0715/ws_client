"""查询历史数据"""

from tap_tools import get_history_datas

request_params = {
    "type": "get",
    "method": "select_topics",
    "exchangeno": "NYMEX",
    "commoditytype": "F",
    "commodityno": "CL",
    "contractno": "2112",
    "begin": "2019-10-29 16:13:00",
    "end": "2019-10-29 17:24:00",
}

history_reports = get_history_datas(request_params)

print(len(history_reports))

for report in history_reports:
    print(report)
    print()

