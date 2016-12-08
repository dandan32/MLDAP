#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 16-12-1 下午9:49
# file: tornado_fetcher.py

from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
import os
import tornado
import logging



logger = logging.getLogger('tornado_fetcher')


class LittleCurlAsyncHTTPClient(CurlAsyncHTTPClient):
    """ Asynchronous HTTP client """
    def free_size(self):
        return len(self._free_list)

    def active_size(self):
        return len(self._curls) - self.free_size()


class LittleSimpleAsyncHTTPClient(SimpleAsyncHTTPClient):
    """ Asynchronous HTTP client """
    def free_size(self):
        return self.max_clients - self.active_size()

    def active_size(self):
        return len(self.active)

""" fetcher's ouput """
fetcher_output = {
    "status_code": int,
    "orig_url": str,
    "url": str,
    "headers": dict,
    "content": str,
    "cookies": dict,
}


class Fetcher(object):

    user_agent = "pyspider/%s (+http://pyspider.org/)" % pyspider.__version__

    default_options = {
        'method': 'GET',
        'headers': {
        },
        'use_gzip': True,
        'timeout': 120,
        'connect_timeout': 20,
    }


    def __init__(self, inqueue, outqueue, poolsize=100, proxy=None, async=True):
        self.inqueue = inqueue 
        self.outqueue = outqueue

        self.poolsize = poolsize
        self._running = False
        self._quit = False
        self.proxy = proxy
        self.async = async
        self.ioloop = tornado.ioloop.IOLoop()
        
        if async:
            self.http_client = LittleCurlAsyncHTTPClient(max_clitent=self.poolsize, io_loop=self.ioloop)
        else:
            self.http_client = tornado.httpclient.HTTPClient(MyCurlAsyncHTTPClient, max_clients=self.poolsize)


