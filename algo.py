# -*- coding: utf-8 -*-

import time
from collections import namedtuple

# 档位
GEAR = namedtuple('GEAR', 'capacity seconds')
MINUTE_GEAR = GEAR(100, 60)
FIVE_MINUTE_GEAR = GEAR(300, 60 * 5)
HOUR_GEAR = GEAR(1500, 60 * 60)

PRESET_BUCKET_TOKEN_RATE = .5
BUCKET_POOL = {}


def token_bucket(ip, capacity, seconds):
    '''
    令牌桶算法举例：
        以IP地址为单位，100次/分钟，300次/五分钟，1500次/小时
    '''
    key = '%s:%s:%s' % (ip, capacity, seconds)
    rate = float(capacity) / seconds
    bucket = BUCKET_POOL.get(key)
    if bucket:
        # 距上次补充令牌过了多少秒
        now = int(time.time())
        pass_second = now - bucket['timestamp_updated']
        # 计算刷新后令牌数
        token_count_flushed = min(int(pass_second * rate) + bucket['token_count'],
                                  capacity)
        bucket['token_count'] = token_count_flushed
        bucket['timestamp_updated'] = now
        if bucket['token_count'] > 0:
            # print bucket['token_count']
            # 用掉一个令牌
            bucket['token_count'] -= 1
            return True
        else:
            return False
    else:
        # 预置半桶令牌 BUCKET_CAPACITY / 2
        BUCKET_POOL[key] = {'token_count': int(capacity * PRESET_BUCKET_TOKEN_RATE)}
        # 用掉一个令牌
        BUCKET_POOL[key]['token_count'] -= 1
        # 记录更新时间
        BUCKET_POOL[key]['timestamp_updated'] = int(time.time())
        return True


def _test_token_bucket_by_gear(ip, gear):
    capacity, seconds = gear.capacity, gear.seconds
    # 用尽半桶令牌
    for i in xrange(int(capacity * PRESET_BUCKET_TOKEN_RATE)):
        assert token_bucket(ip, capacity, seconds) is True
    # 多一枚也没有了
    assert token_bucket(ip, capacity, seconds) is False
    # 等待6秒 又多了 6 * rate个令牌
    sleep_seconds = 6
    time.sleep(sleep_seconds)
    rate = float(capacity) / seconds
    for i in xrange(int(sleep_seconds * rate)):
        assert token_bucket(ip, capacity, seconds) is True
    # 多一枚也没有了
    assert token_bucket(ip, capacity, seconds) is False


def test_token_bucket():
    ip = '0.0.0.0'
    _test_token_bucket_by_gear(ip, MINUTE_GEAR)
    _test_token_bucket_by_gear(ip, FIVE_MINUTE_GEAR)
    _test_token_bucket_by_gear(ip, HOUR_GEAR)


def is_internal_ip(ip):
    _ip = reduce(lambda x, y: (x << 8)+y, map(int, ip.split('.')))
    print _ip, type(_ip)
    return _ip >> 24 == 10 or _ip >> 20 == 2753 or _ip >> 16 == 49320


if __name__ == '__main__':
    # test_token_bucket()
    print is_internal_ip('192.168.0.1')
    print is_internal_ip('10.2.0.1')
    print is_internal_ip('172.16.1.1')
