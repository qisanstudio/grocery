# -*- coding: utf-8 -*-

import asyncio
import requests
from logformat import get_color_console_logger


logger = get_color_console_logger(__name__)



async def f1():
    logger.info('f1 start')
    await asyncio.sleep(1)
    logger.info('f1 end')


async def f2():
    logger.info('f2 start')
    await asyncio.sleep(1)
    logger.info('f2 end')


def test_asyncio():
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    tasks = [
        asyncio.ensure_future(f1()),
        asyncio.ensure_future(f2())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    test_asyncio()
