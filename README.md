### logformat.py

```
from logformat import get_color_file_logger
logger = get_color_file_logger(__name__)

# from logformat import get_color_console_logger
# logger = get_color_console_logger(__name__)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

![本来是效果图](http://3-im.guokr.com/auLjVuJNnb1w4_ByAvg5VLSDUws5yij151zwBGVSVBrcBAAAqQAAAFBO.png)

```
# shortcut example
clogger = get_color_file_logger('clogger', file_name='/var/log/zydebug.log')
# use like
from logformat import clogger
```

### rw.py
```
# 读csv文件转成List
csv_reader('input_filename.csv')

# List转成csv文件
csv_reader('output_filename.csv', rows=[('a', 1), ('b', 2)])
```


### markdown文件夹
一些技术点的专题总结
version 说明完成度 1.0可使用版

#### 总结分三步:
    1. 二八原理：先把那些经常用到的总结记录下来。不会的时候就来查。
    2. 总结规律原理，记录在脑海里，最好能分享出去。
    3. 有些东西如果做到了如指掌，就需要实现一次此工具。


### TODO LIST

#### Redis
    1. 继续梳理下Redis里面的key，看看还有哪些key需要加expire，以及可能造成内存泄露的key，尤其是list类型的。
    2. ps: 定时更新待查询的：eg：每日排行榜/sitemap, 所有key应该都有过期时间

#### SQLAlchemy
    1. alembic
    2. views/mixins.py
    3. db.undefer('current_user_has_supported')

#### Docker
    1. 起源 & 进化 & 原理
    2. 具体如何操作的？
    3. 科学人如何应用的？
    4. 未来如何跟进？

#### Guokrplus
    1. 验证码的实现

#### Postgres
    1. mapper
    2. listener
    3. 另，为啥limit变成5000cpu就不行了，变成50就可以了呢？

#### Linux cmd - 搜索

#### Linux cmd - 权限

#### Linux cmd - 网络

#### Linux cmd - 软件维护

#### Linux cmd - 磁盘空间不足

#### Linux cmd - 清除

#### Linux cmd - 进程管理
killall 进程名

#### Nginx
    1. Nginx常用语法
    2. 实战修改guokr Nginx配置

#### Python
    1. isinstance(subdomain, (list, tuple, set))
    2. reduce / filter / map + import operator filter(None, questions) 道理？
    3. 属性映射url的实现 group.member.get(limit=20) => /group/member?limit=20

#### Atom

#### VIM

#### Flask


#### 扩展记录
    AOP 编程思想
