#### version 0.1

### redis的一些操作
#### generic
    1.

#### Strings
    1. GET操作：GET/GETRANGE/MGET
    2. SET操作：SET/SETRANGE/MSET/MSETNX/PSETEX/SETEX/SETNX
    3. 其他基本操作：APPEND/STRLEN/GETSET
    4. 可以按bit操作：BITCOUNT/BITFIELD/BITOP/BITPOS/GETBIT/SETBIT等操作。可以利用position和0/1开关实现一些功能，比如用户在线人数/天，优点是省空间。
    5. 可以自动识别integer/float类型。对应操作：DECR/DECRBY/INCR/INCRBY/INCRBYFLOAT

#### Lists
    1. 一些基本操作：LLEN/LREM
    2. 此类型可以左右弹出数据：LPOP/RPOP, 还可以阻塞弹出：BLPOP/BRPOP
    3. 还可以左右压入数据：LPUSH/RPUSH, 可以仅当key存在的时候压入数据：LPUSHX/RPUSHX, 还可以从一个list弹出直接压入到另一个list里：RPOPLPUSH/BRPOPLPUSH
    4. 针对index的一些操作：LINDEX/LSET/LTRIM/LRANGE
    5. 一个特殊操作，可以在某个value的前后插入value：LINSERT

#### Sets
    1. 一些基本操作：SADD/SCARD/SMEMBERS/SISMEMBER/SREM
    2. 随机弹/取count个元素：SPOP/SRANDMEMBER
    3. 集合之间的一些操作：SDIFF/SINTER/SUNION
    4. 直接创建新集合的操作: SDIFFSTORE/SINTERSTORE/SMOVE/SUNIONSTORE

#### Sorted Sets
    1. 基本操作：ZADD/ZCARD/ZSCORE/ZINCRBY、ZCOUNT/ZLEXCOUNT
    2. 集合操作：ZINTERSTORE/ZUNIONSTORE
    2. 获取操作：ZRANGE/ZREVRANGE、ZRANGEBYLEX/ZREVRANGEBYLEX、ZRANGEBYSCORE/ZREVRANGEBYSCORE
    3. 删除操作：ZREM/ZREMRANGEBYLEX/ZREMRANGEBYRANK/ZREMRANGEBYSCORE
    4. 排序操作：ZRANK/ZREVRANK
    5. ZSCAN

#### Hashes
    1. 读操作：HGET/HMGET/HEXISTS/HSTRLEN
    2. 写操作：HSET/HMSET/HSETNX
    3. 只针对key的操作：HKEYS/HGETALL/HVALS/HLEN
    4. 删除操作：HDEL
    5. 自动识别integer/float类型。对应操作：HINCRBY/HINCRBYFLOAT
    6. HSCAN

### 主站的redis常用操作总结



### redis高级应用 pub/sub 模式
