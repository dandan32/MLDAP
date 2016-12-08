#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 16-12-5 下午5:08
# file: ioloop_utils.py.py

import tornado.ioloop
import tornado.httpserver
import tornado.wsgi
import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


def PeriodicCallback(func, callback_time=100, io_loop=None):
    """
    封装 tornado.ioloop.PeriodicCallback 函数
    以 callback_time 毫秒为周期调用 func 函数
    :param func:
    :param callback_time:
    :param io_loop:
    :return:
    """
    if io_loop is None:
        io_loop = tornado.ioloop.IOLoop()
    p_func = tornado.ioloop.PeriodicCallback(func, callback_time, io_loop)
    p_func.start()
    return io_loop, p_func

def HTTPServer(host='', port='8080', app=None, io_loop=None, ):
    """
    封装HTTPServer,
    给定单进程
    :param host:
    :param port:
    :param app:
    :param io_loop:
    :return: io_loop
    """
    if app is None:
        raise ValueError("app must not be None.")
    container = tornado.wsgi.WSGIContainer(app)
    if io_loop is None:
        server = tornado.httpserver.HTTPServer(container)
        server.bind(port=port, address=host)
        server.start(0)
    else:
        server = tornado.httpserver.HTTPServer(container, io_loop=io_loop)
        server.listen(port=port, address=host)
    print('%s listening on %s:%s', app.__name__, host, port)
    return io_loop

if __name__ == '__main__':

    def function_for_test():
        import time
        print time.time()

    # p_ioloop = tornado.ioloop.IOLoop()
    # p_ioloop, p_func = PeriodicCallback(function_for_test, 1000, p_ioloop)
    # print p_func.is_running()
    # p_ioloop.start()


    def application_for_test(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        import time
        time.sleep(2)
        return '%s, %s' % (time.time(), __name__)

    def run_in_process():
        HTTPServer(app=application_for_test)
        tornado.ioloop.IOLoop.current().start()

    import multiprocessing

    process = multiprocessing.Process(target=run_in_process)
    process.start()

    def run_requests():
        import requests
        import time
        while True:
            print '1, %s' % requests.get('http://127.0.0.1:8080').text

    def run_requests2():
        import requests
        import time
        while True:
            print '2, %s' % requests.get('http://127.0.0.1:8080').text




    for i in range(2):
        multiprocessing.Process(target=run_requests).start()
        multiprocessing.Process(target=run_requests2).start()


    process.join()
