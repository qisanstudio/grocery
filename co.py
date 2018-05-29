import time
# import gevent
import logging
import multiprocessing
# from gevent import monkey

from logformat import get_color_concurrent_logger


# monkey.patch_socket()

logger = get_color_concurrent_logger('test_csv_format_log',
                                     file_name='test_csv_format_log.csv',
                                     level=logging.INFO,
                                     fmt='%(message)s')


def remote(url):
    pass


def f(display):
    for i in xrange(100):
        time.sleep(i % 3)
        logger.info('%s,%s' % (display, i))


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=16)

    for disp in ['one', 'two', 'three', 'four'] * 40:
        pool.apply_async(f, (disp, ))

    pool.close()
    pool.join()
