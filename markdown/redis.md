#### version 0.1

### 思考
#### 用redis都能缓冲什么？
1. 服务器的外网请求，比如qiniu
2. 数据库的数据

#### 怎么定义冷热数据？

#### 如何监控redis
1. 大小
2. 吞吐量

#### 能带来多少性能的提升？

#### 缓存高可用？


### 果壳主站调研
#### gkapp-censor
1. 利用redis的过期时间做短时间禁言功能 TTL/SETEX
2. user_context.py 用来做缓存的，没看明白

#### gkapp-image
1. 缓存qiniu的token GET/SET/EXPIRE (七牛的token也有过期时间，把redis key的过期设置的小一点，确保缓存的token可用)
2. 用HASH结构来存储生成的图片信息，没有过期时间自己维护其大小。 HSET/HDEL/HGET

#### gkapp-auth
1. redis pipeline 操作 auth/models/token.py 多类型合作完成
2. 重置密码申请操作 类似gkapp-censor.1
3. 验证码的实现 auth/views/captcha.py
4. 手机验证码的实现 借助 INCR/EXPIRE 实现频繁请求报错
5. 白名单的实现 SET/GET/DELETE/KEYS
6. 借助内存完成接口级别的信息传递，批量发信息用key作为锁 auth/backends/message.py SET/SETNX/DELETE/EXPIRE

#### gkapp-handpick
1. 大转盘 lottery.py
2. 缓冲精选文章，不那么频繁更新的 HSET/HGETALL/EXPIRE

#### gkapp-group
1. hook.py 缓冲计数  EXISTS/INCR/SETEX
2. 禁言 string类型
3. models/user.py +134 使用错误

#### gkapp-community
1. 黑名单实现 sortedset    ZADD/EXPIRE/ZCARD/ZRANGE/ZREM/ZRANK
2. activity缓存  sortedset    zrevrange/zremrangebyrank/expire/zcard/zadd/delete

#### guokr-core
1. 缓存网页，然后Response sitemaps.py
2. 频率控制器    sortedset 按时间排序 一定间隔时间内统计次数
3. session
4. USER_META hash


#### 管理redis大小
1. 设置过期时间
2. 先评估每种类型的大小，之后预估大小。比如：用户相关的统计，到达一定规模能很快计算出来他所占用空间
3. 删除操作通常通过管道执行


#### redis key 命名规则


### redis的一些操作
#### generic
    1.
    2.

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

#### 关于过期时间的操作
    1. TTL/EXPIRE/PEXPIRE、PERSIST、SETEX/PSETEX、EXPIREAT/PEXPIREAT
    2. 会移除生存时间的操作： DEL/SET/GETSET
    3. 只修改key或value不影响生存周期的操作：INCR/LPUSH/HSET/RENAME

### 一些用到redis的需求汇总
    1.


### redis高级应用 pub/sub 模式


### 前人经验
    1. 表达从属关系（一对多，多对多），最好用集合； 比如： 书名和标签，关注与被关注（微博粉丝关系）等等。
    2. 求最近的，一般利用链表后入后出的特性。比如：最近N个登录的用户，可以维护一个登录的链表，控制他的长度，使得里面永远保存的是最近的N个登录用户。
    3. 对于排序，积分榜这类需求，可以用有序集合，比如：我们把用户和登录次数统一存储在一个sorted set里，然后就可以求出登录次数最多用户。
    4. 对于大数据量的非是即否关系，还可以通过位图（setbit）的方式，比如：1亿个用户, 每个用户 登陆/做任意操作,记为今天活跃,否则记为不活跃；（每天一个位图来记录，会员id就是位图的位置）；
