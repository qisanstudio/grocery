#### version 0.5.3


#### REDIS KEY 命名规则
Redis key值是二进制安全的
1. 太长会增加内存的消耗，查找成本会很高
2. 太短也不要损失可读性
3. 坚持一个模式。object-type:\id:field.words (comment:\1234:reply.to)


#### 用REDIS都做了些什么？
##### 利用key的过期特性：
1. 验证码
2. 短时间禁言
3. 密码重置邮件
4. 数据冷热分离

验证码例子：手机号50秒内验证登录
```
phone_number, action = 15311223344, 'login'
redis_key = 'AUTH:PHONE:RANDOM_CODE:%s:%s' % (phone_number, action)
# 检查的同时设置redis_key
if redis.incr(redis_key) > 1:
    return "Send verify code to frequently."
redis.expire(redis_key, 50)
```

##### 减少站外请求：
1. 缓存token（qiniu、weixin）

TOKEN例子：七牛token缓存
```
def generate_token():
    redis_key = 'QINIU:UPLOAD_TOKEN'
    qiniu_upload_token = redis.get(redis_key)
    if qiniu_upload_token:
        return qiniu_upload_token

    qiniu_upload_token = _get_qiniu_upload_token()
    redis.set(redis_key, qiniu_upload_token)
    redis.expire(redis_key, 21000)

    return qiniu_upload_token
```

##### 减少站内请求：
1. 信息流
2. 热数据缓存（user_meta）

用户信息流例子：activity
```
class _ActivitySortedSet(object):

    rkey_tpl = None
    expire_in_seconds = 4 * 24 * 60 * 60  # 限定动态钉在内存的最长时间为4天
    limited_size = 5000  # 限定动态最大长度为5000条

    def __init__(self, ukey):
        self.ukey = ukey
        self.rkey = self.rkey_tpl % self.ukey

    @property
    def count(self):
        return redis.zcard(self.rkey)

    @locked_cached_property
    def user(self):
        return UserModel.query.get(self.ukey)

    def activate(self):
        '''
        设定过期时间
        '''
        redis.expire(self.rkey, self.expire_in_seconds)

    def trim(self):
        '''
        瘦身
        '''
        redis.zremrangebyrank(self.rkey, 0, -self.limited_size - 1)

    def retrieve(self, limit, offset=0):
        """返回列表

        函数会主动清理被删除的对象, 并补齐 limit 长度
        极端情况下会循环 total_count / limit 次

        :Parameters
            - limit (unsigned int) 一次返回数量
            - offset (unsigned int) 偏移量

        :Returns
            ActivityModel 对象列表

        """
        _tbl = ActivityModel
        returns = []

        removed = []
        while len(returns) < limit:
            activity_ids = redis.zrevrange(self.rkey, offset,
                                           offset + limit)
            if not activity_ids:
                # 这里很重要, 不能再获取到说明已经到末尾了,
                # 必须跳出循环, 否则会死循环的
                break
            activity_ids = map(int, activity_ids)  # 脏数据咋办?
            activities = _tbl.query.filter(
                _tbl.id.in_(activity_ids)).all()
            activities = {a.id: a for a in activities}
            _removed = []
            for aid in activity_ids:
                try:
                    returns.append(activities[aid])
                except KeyError:
                    _removed.append(aid)
            offset += limit
            removed += _removed
        if removed:
            self.delete(*removed)
        self.trim()
        self.activate()
        return returns[:limit]

    def retrieve_by_client_id(self, limit, client_ids=[]):
        """返回与指定client相关的动态列表

        鉴于性能考虑，有可能取不够需要数量的动态(夭折)
        这是个很操蛋的函数，请仔细勘酌、谨慎使用

        :Parameters
            - limit (unsigned int) 一次返回数量
            - client_ids (unsigned int) 应用的source_client_id列表

        :Returns
            ActivityModel 对象列表

        """
        _tbl = ActivityModel
        query = _tbl.query
        if client_ids:
            query = query.filter(_tbl.source_client_id.in_(client_ids))
        returns = []

        batch_num = 100  # 一次性从redis中批量取出的数量
        current_offset = 0  # 当前的redis列表的偏移量

        max_loop = 5  # 最多从redis中批量取5次，要是取的数据不够那也不取了
        loop_count = 0  # 当前批量取的次数

        while len(returns) < limit and loop_count < max_loop:
            activity_ids = redis.zrevrange(self.rkey, current_offset,
                                           current_offset + batch_num)
            if not activity_ids:
                # 这里很重要, 不能再获取到说明已经到末尾了,
                # 必须跳出循环, 否则会死循环的
                break
            activity_ids = map(int, activity_ids)  # 脏数据咋办?
            activities = query.filter(
                _tbl.id.in_(activity_ids)).all()
            activities = {a.id: a for a in activities}
            for aid in activity_ids:
                try:
                    returns.append(activities[aid])
                except KeyError:
                    pass
            current_offset += batch_num
            loop_count += 1
        self.trim()
        self.activate()
        return returns[:limit]

    def create(self):
        """创建该用户的动态索引表

        根据该用户关注的对象创建订阅动态列表, 可能比较慢

        :Returns
            已创建订阅动态列表的长度

        """
        user = self.user
        if user is None:
            return  # wtf ?!
        activities = self._retrieve_all(user)
        activities = [(str(a.id), int(a.date_created.strftime('%s')))
                      for a in activities]
        if activities:
            activities = dict(activities)
            result = redis.zadd(self.rkey, **activities)
        else:
            result = 0
        return result

    def delete(self, *activity_ids):
        """从该用户的动态索引表中删除

        :Parameters:
            - activity_ids (int): 将被删除的动态id

        :Returns:
            实际操作行数

        """
        with redis.pipeline() as pipe:
            pipe.zrem(self.rkey, *activity_ids)
            count, = pipe.execute()
        return count

    def delete_all(self):
        """ 删除该用户的所有动态索引
            目前只有删除用户时才会用到
        """
        redis.delete(self.rkey)

    def _retrieve_all(self, user):
        """继承此方法实现获取动态列表的功能"""
        raise NotImplementedError


class ActivityFeedList(_ActivitySortedSet):
    rkey_tpl = 'user-activity-feeds:%s'

    def _retrieve_all(self, user):
        followings = user.followings
        ukey_followings = [f.ukey for f in followings]
        ukey_followings.append(user.ukey)
        _tbl = ActivityModel
        return (_tbl.query
                .with_entities(_tbl.id, _tbl.date_created)
                .filter(_tbl.user_ukey.in_(ukey_followings))
                .order_by(_tbl.date_created.desc())
                .limit(self.limited_size)
                .all())
```


##### 应用间协同工作：
1. sitemap
2. session

网站地图例子：
home应用下后台人工设置活跃小组文章，把post_id放到redis里
```
def share_post_url(self, pid):
    if not shared_redis.exists('SITEMAP::BAIDU_SEARCH::POST::IDS'):
        h = UserHonorModel.query.filter(
            UserHonorModel.kind == 'post'
        ).order_by(UserHonorModel.date_created.asc()).all()
        for i in h:
            shared_redis.rpush(
                'SITEMAP::BAIDU_SEARCH::POST::IDS', i.resource_id)
    shared_redis.rpush(
        'SITEMAP::BAIDU_SEARCH::POST::IDS', pid)
```

group应用每天定时取post_id后，取出所有百度爬虫需要的信息放到redis里
```
class BaiduSearchSiteMapAPI(RESTfulBackendAPI):
    resource_path = '/sitemap/baidu_search'
    page_limit = 500

    redis_ids = 'SITEMAP::BAIDU_SEARCH::POST::IDS'
    redis_maxid_key = 'SITEMAP::BAIDU_SEARCH::GROUP::MAXID'
    redis_curid_key = 'SITEMAP::BAIDU_SEARCH::GROUP::CURRENT'
    redis_data_key = 'SITEMAP::BAIDU_SEARCH::GROUP::DATA'

    @property
    def maxid(self):
        maxid_redis_key = self.redis_maxid_key
        return int(shared_redis.get(maxid_redis_key) or '0')

    def clean_ids(self):
        maxid_redis_key = self.redis_maxid_key
        shared_redis.delete(maxid_redis_key)
        curid_redis_key = self.redis_curid_key
        shared_redis.delete(curid_redis_key)

    def content_filter(self, content):
        content = BeautifulSoup(content).text
        reg = r"[<>&'\"\x00-\x08\x0b-\x0c\x0e-\x1f]"
        content = re.sub(reg, '', content)
        return content

    def create(self):
        now = datetime.now()
        maxid = self.maxid
        if not maxid:
            maxid = shared_redis.llen(self.redis_ids)
            maxid_redis_key = self.redis_maxid_key
            shared_redis.set(maxid_redis_key, maxid)

        curid_redis_key = self.redis_curid_key
        curid = int(shared_redis.get(curid_redis_key) or '0')
        after = curid + self.page_limit

        if curid >= maxid:
            self.clean_ids()
            return

        data_redis_key = self.redis_data_key
        ids = shared_redis.lrange(self.redis_ids, curid, after)
        posts = [PostModel.query.get(i) for i in ids]
        posts = filter(None, posts)

        preload_user_meta(posts, 'ukey_author')
        for i, a in enumerate(posts):
            author = user_meta(a.ukey_author)
            tmp = {
                'loc': a.url,
                'lastmod': now.strftime('%Y-%m-%d'),
                'changegfreq': 'monthly',
                'docurl': a.url,
                'title': a.title,
                'abstract': a.summary,
                'content': self.content_filter(
                    a.content),
                'field': '',
                'date': a.date_created.strftime('%Y-%m-%d'),
                'qualitylevel': 2,
                'author': author.get('nickname', ''),
                'authorimg': author.get('avatar', {}).get('small', ''),
                'authorurl': author.get('url'),
                'authorinfo': author.get('title'),
                'source': '果壳小组',
                'readnum': a.replies_count * 200 * random.randint(
                    10, 30) + random.randint(1, 999),
                'comnum': a.replies_count,
                'likenum': a.likings_count,
                'recommnum': a.recommends_count,
                'concernednum': a.recommends_count,
            }
            shared_redis.rpush(data_redis_key, json.dumps(tmp))
        shared_redis.set(curid_redis_key, after)
        b_group.sitemap.baidu_search.create(_delay=30)
```


##### 其它功能：
1. 频率控制器(sortedset)
2. 可再生数据存储(公式图片)

频率控制器例子
```
def set(self):
    """增加一次操作计数, 然后检查是否触发频率控制

    :Returns
        True: 没有触发频率控制
        False: 已触发频率控制

    """
    enable = app.config.get('ENABLE_THRESHOLD_CONTROL', True)
    if app and not enable:
        return True  # 频率控制关闭时始终允许
    if isinstance(enable, basestring) and enable.lower() == 'always':
        return False
    now = time.time()
    with redis.pipeline() as rp:
        expire_at = now - self.timeout
        rp.zremrangebyscore(self.rkey, 0, expire_at)
        rp.zadd(self.rkey, now, now)
        rp.zcount(self.rkey, expire_at, now)
        # 将过期时间定位到当前时间往后 timeout 秒
        rp.expire(self.rkey, self.timeout)
        _, _, count, _ = rp.execute()

    return count <= self.maximum
```


### 主站用到redis的地方汇总
#### gkapp-censor
1. 利用redis的过期时间做短时间禁言功能 TTL/SETEX
2. user_context.py 用来做缓存的，没看明白

#### gkapp-image
1. _缓存qiniu的token GET/SET/EXPIRE (七牛的token也有过期时间，把redis key的过期设置的小一点，确保缓存的token可用)_
2. 用HASH结构来存储生成的图片信息，没有过期时间自己维护其大小。 HSET/HDEL/HGET

#### gkapp-auth
1. redis pipeline 操作 auth/models/token.py 多类型合作完成
2. 重置密码申请操作 类似gkapp-censor.1
3. 验证码的实现 auth/views/captcha.py
4. _手机验证码的实现 借助 INCR/EXPIRE 实现频繁请求报错_
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
2. _activity缓存  sortedset    zrevrange/zremrangebyrank/expire/zcard/zadd/delete_

#### guokr-core
1. 缓存网页，然后Response sitemaps.py
2. 频率控制器    sortedset 按时间排序 一定间隔时间内统计次数
3. session
4. USER_META hash


### 常见使用错误
1. 忘记设置过期时间
```
redis_key = app.config['AUTH_REDIS']['phone_random_code'] % (
    phone, action_type
)
# 检查的同时设置redis_key
if redis.incr(redis_key) > 1:
    # 历史遗留问题，线上有些redis并没有及时的设置缓存时间
    redis.expire(redis_key, 50)
    raise APIBadRequest(
        290018, "Send verify code to frequently.")
redis.expire(redis_key, 50)
```

2. 未设置过期时间的没有检查机制
SITEMAP

3. 数据类型选择不当
白名单功能
```
shared_redis.set('realname_whitelist:%s' % target.ukey, 1)  # 不恰当
shared_redis.hset('realname_whitelist', target.ukey, 1)  # 恰当
```
不恰当理由:
1. string类型如果想遍历需要keys操作，而这个是要在生产环境的大数据中尽量避免的
2. 内存宝贵，hash更省空间

一些网上搜到的关于redis类型选择的经验总结:

    1. 表达从属关系（一对多，多对多），最好用集合； 比如： 书名和标签，关注与被关注（微博粉丝关系）等等。
    2. 求最近的，一般利用链表后入后出的特性。比如：最近N个登录的用户，可以维护一个登录的链表，控制他的长度，使得里面永远保存的是最近的N个登录用户。
    3. 对于排序，积分榜这类需求，可以用有序集合，比如：我们把用户和登录次数统一存储在一个sorted set里，然后就可以求出登录次数最多用户。
    4. 对于大数据量的非是即否关系，还可以通过位图（setbit）的方式，比如：1亿个用户, 每个用户 登陆/做任意操作,记为今天活跃,否则记为不活跃；（每天一个位图来记录，会员id就是位图的位置）；

### 一些可优化点
1. 能用数字就用数字，用字符串会增加空间使用
2. 尽量不要有sort操作
3. 避免有些不必要的操作，时间复杂度
4. 删除操作通常通过管道执行，节省在网络延迟的时间。

--------
# 二八原理redis操作再总结

### redis的一些操作
#### generic
    1. KEYS 支持通配符*?, **不建议在生产环境大数据量下使用**
    2. MOVE/MIGRATE(实例内从此db到彼db/从此实例到彼实例)，RANDOMKEY，TYPE/Object(Key的类型/对象编码类型，空置时间)，DUMP/RESTORE(value值的持久化)

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
    1. TTL/EXPIRE/PEXPIRE、PERSIST、SETEX/PSETEX、EXPIREAT/PEXPIREAT（默认以秒为单位，P开头的毫秒为单位）
    2. 会移除生存时间的操作： DEL/SET/GETSET
    3. 只修改key或value不影响生存周期的操作：INCR/LPUSH/HSET/RENAME

### 一些用到redis的需求汇总
    1.


### redis高级应用 pub/sub 模式




### 关于redis一些问题的思考
#### 怎样使用redis，才更节约内存？
