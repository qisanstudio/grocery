# -*- coding: utf-8 -*-

import requests
import unittest
# from urllib import urlencode, quote #python2
from urllib.parse import urlencode


# URI详细介绍 https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Generic_syntax


class APIError(Exception):

    def __init__(self, error):
        self.error = error
        StandardError.__init__(self, error)
    
    def __str__(self):
        return 'APIError: {}'.format(self.error)


class APIClient(object):

    def __init__(self, path=''):
        self._base_url = path
    
    def __getattr__(self, item):
        name = '{}/{}'.format(self._base_url, item)
        return _Callable(self, name)
    

class _Excutable(object):

    def __init__(self, client, method, path):
        self._client = client
        self._method = method.upper()
        self._path = path

    def __call__(self, **kw):
        querys = kw.pop('querys')
        if querys:
            url = '{}?{}'.format(self._client._base_url, urlencode(querys))
        else:
            url = self._client._base_url

        return requests.request(self._method, url, **kw)

    def __str__(self):
        return '_Excutable({} {})'.format(self._method, self._path)

    __repr__ = __str__


class _Callable(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name
    
    def __getattr__(self, item):
        if item == 'get':
            return _Excutable(self._client, 'GET', self._name)
        elif item == 'post':
            return _Excutable(self._client, 'POST', self._name)
        name = '{}/{}'.format(self._name, item)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__


class TestAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('http://www.api.com:8000')

    def test_urls(self):
        self.assertEqual(self.client.a.b._name, "http://www.api.com:8000/a/b")


if __name__ == '__main__':
    unittest.main()
