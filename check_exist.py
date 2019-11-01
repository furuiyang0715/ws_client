"""获取存在历史数据的topic"""

from tap_tools import get_exists_topics

ret = get_exists_topics()

print(ret)

print(len(ret))
