"""获取60s内活跃的 topic（即60s有数据推送），可订阅，有历史数据"""

from tap_tools import get_active_topics

ret = get_active_topics()

print(ret)